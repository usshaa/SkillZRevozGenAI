import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from memory.memory_manager import count_tokens, manage_short_term_memory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def test_count_tokens():
    msgs = [HumanMessage(content="Hello world!")]
    # 2 words * 1.3 = 2.6 -> 2
    assert count_tokens(msgs) == 2

def test_manage_memory_truncate():
    msgs = [
        SystemMessage(content="You are an AI."),
        HumanMessage(content="This is a long message to truncate out."),
        AIMessage(content="Yes, quite long."),
        HumanMessage(content="Short msg")
    ]
    
    # Force max tokens to 10 and strategy to truncate
    new_msgs = manage_short_term_memory(msgs, override_strategy="truncate", override_max_tokens=10)
    
    assert len(new_msgs) < len(msgs)
    assert isinstance(new_msgs[0], SystemMessage)
    assert isinstance(new_msgs[-1], HumanMessage)
    assert new_msgs[-1].content == "Short msg"
