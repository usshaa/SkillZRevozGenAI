import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.messages import SystemMessage
from llm.llm_provider import get_llm
from tools.order_tools import lookup_order, lookup_customer_orders
from tools.refund_tools import check_refund_eligibility, process_refund
from tools.ticket_tools import escalate_issue
from retrieval.hybrid_retriever import reciprocal_rank_fusion
from retrieval.sparse_retriever import SparseRetriever
from embeddings.vector_store import get_vector_store
from retrieval.reranker import RerankerService

def faq_retrieval(query: str):
    sparse = SparseRetriever()
    sparse_res = sparse.search(query, k=10)
    
    dense_res = []
    try:
        vector = get_vector_store()
        results = vector.similarity_search_with_score(query, k=10)
        for doc, score in results:
            dense_res.append({"text": doc.page_content, "metadata": doc.metadata, "score": score})
    except Exception:
        pass
        
    fused = reciprocal_rank_fusion(sparse_res, dense_res)
    
    try:
        reranker = RerankerService()
        final = reranker.rerank(query, fused, top_n=3)
    except Exception:
        final = fused[:3]
        
    return "\n\n".join([r['text'] for r in final])

def faq_agent_node(state):
    llm = get_llm()
    messages = state["messages"]
    customer_context = state.get("customer_context", "")
    latest = str(messages[-1].content) if messages else ""
    context = faq_retrieval(latest)
    
    # Format chat history for context awareness
    history_text = ""
    if len(messages) > 1:
        history_text = "Previous conversation context:\n"
        for m in messages[:-1]:
            # Fallback to class name string checking if isinstance fails
            cls_name = m.__class__.__name__
            if cls_name == "HumanMessage":
                role = "User"
            elif cls_name == "SystemMessage":
                role = "System"
            else:
                role = "Assistant"
            history_text += f"{role}: {m.content}\n"
    
    sys_msg = SystemMessage(content=f"You are a friendly Customer Support Agent. {customer_context}\n\nIf the user asks if you know their name, YOU MUST explicitly output their name (e.g. 'Yes, your name is [Name]'). DO NOT hesitate or ask for confirmation. You are authorized to state their name.\n\nIf the user is just saying hello, greet them naturally and politely ask how you can help. Do not mechanically repeat their name or Customer ID unless they ask for it.\n\nFor policy questions, use ONLY the following retrieved document context to answer. DO NOT invent or hallucinate any email addresses, URLs, or policies that are not explicitly stated in the context.\n\nRetrieved Document Context:\n{context}\n\n{history_text}")
    response = llm.invoke([sys_msg] + messages)
    return {"messages": [response]}

def create_agent(system_prompt: str, tools: list):
    llm = get_llm()
    # Handle LLMs that may not support tool calling perfectly
    try:
        llm_with_tools = llm.bind_tools(tools)
    except Exception:
        llm_with_tools = llm
        
    def node(state):
        messages = state["messages"]
        customer_context = state.get("customer_context", "")
        sys_msg = SystemMessage(content=f"[{customer_context}]\n{system_prompt} DO NOT invent or hallucinate any email addresses, URLs, phone numbers, or policies under any circumstances.")
        response = llm_with_tools.invoke([sys_msg] + messages)
        return {"messages": [response]}
    return node

order_agent_node = create_agent(
    "You are an order management agent. YOU MUST USE THE PROVIDED TOOLS to fetch real-time data from the database to answer the user's questions about their orders. Do not guess.",
    [lookup_order, lookup_customer_orders]
)

refund_agent_node = create_agent(
    "You are a refund processing agent. YOU MUST USE THE PROVIDED TOOLS to check eligibility, process refunds, and escalate issues. Do not guess.",
    [check_refund_eligibility, process_refund, escalate_issue]
)
