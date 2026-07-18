import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import SHORT_TERM_MAX_TOKENS, SHORT_TERM_STRATEGY
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from llm.llm_provider import get_llm

def count_tokens(messages):
    total_words = sum(len(str(m.content).split()) for m in messages)
    return int(total_words * 1.3)

def summarize_messages(messages):
    llm = get_llm()
    history = "\n".join([f"{type(m).__name__}: {m.content}" for m in messages])
    prompt = f"Summarize the following conversation history briefly while retaining key details:\n\n{history}"
    summary = llm.invoke(prompt)
    return [SystemMessage(content=f"Summary of past conversation: {summary.content}")]

def manage_short_term_memory(messages, override_strategy=None, override_max_tokens=None):
    strategy = override_strategy or SHORT_TERM_STRATEGY
    max_tokens = override_max_tokens or SHORT_TERM_MAX_TOKENS
    
    if not messages:
        return []
        
    token_count = count_tokens(messages)
    if token_count <= max_tokens:
        return messages
        
    if strategy == "summarize":
        system_msg = []
        if messages and isinstance(messages[0], SystemMessage):
            system_msg = [messages[0]]
            messages = messages[1:]
            
        last_msg = messages[-1]
        to_summarize = messages[:-1]
        
        if not to_summarize:
            return system_msg + [last_msg]
            
        summary_msg = summarize_messages(to_summarize)
        return system_msg + summary_msg + [last_msg]
        
    elif strategy == "truncate":
        current_tokens = count_tokens(messages)
        truncated = messages[:]
        while current_tokens > max_tokens and len(truncated) > 1:
            if len(truncated) > 1 and isinstance(truncated[0], SystemMessage):
                truncated.pop(1)
            else:
                truncated.pop(0)
            current_tokens = count_tokens(truncated)
        return truncated
        
    return messages
