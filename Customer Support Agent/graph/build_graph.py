import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from llm.llm_provider import get_llm
from graph.state_schema import AgentState
from graph.agents import faq_agent_node, order_agent_node, refund_agent_node
from tools.order_tools import lookup_order, lookup_customer_orders
from tools.refund_tools import check_refund_eligibility, process_refund
from tools.ticket_tools import escalate_issue
from memory.checkpoint_setup import get_checkpointer

def supervisor_node(state: AgentState):
    llm = get_llm()
    messages = state["messages"]
    
    system_prompt = (
        "You are a supervisor routing user requests to one of three workers: 'faq', 'order', or 'refund'. "
        "Look at the LATEST user message. "
        "If they ask about general policies, rules, FAQs, or return periods, output 'faq'. "
        "If they ask to check, find, or track a specific order, output 'order'. "
        "If they explicitly ask for a refund, return, or to escalate to a human, output 'refund'. "
        "Output ONLY the exact name of the worker."
    )
    
    response = llm.invoke([SystemMessage(content=system_prompt)] + messages)
    decision = str(response.content).strip().lower()
    
    if 'faq' in decision:
        next_node = 'faq'
    elif 'order' in decision:
        next_node = 'order'
    elif 'refund' in decision:
        next_node = 'refund'
    else:
        next_node = 'faq' # Default fallback
        
    return {"next": next_node}

def build_support_graph():
    workflow = StateGraph(AgentState)
    
    # Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("faq", faq_agent_node)
    workflow.add_node("order", order_agent_node)
    workflow.add_node("refund", refund_agent_node)
    
    # Tool nodes
    order_tools = ToolNode([lookup_order, lookup_customer_orders])
    refund_tools = ToolNode([check_refund_eligibility, process_refund, escalate_issue])
    
    workflow.add_node("order_tools", order_tools)
    workflow.add_node("refund_tools", refund_tools)
    
    # Edges
    workflow.add_edge(START, "supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "faq": "faq",
            "order": "order",
            "refund": "refund",
            "FINISH": END
        }
    )
    
    workflow.add_edge("faq", END)
    
    def order_router(state):
        messages = state["messages"]
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return END
        
    workflow.add_conditional_edges(
        "order",
        order_router,
        {"tools": "order_tools", END: END}
    )
    workflow.add_edge("order_tools", "order")
    
    def refund_router(state):
        messages = state["messages"]
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return END
        
    workflow.add_conditional_edges(
        "refund",
        refund_router,
        {"tools": "refund_tools", END: END}
    )
    workflow.add_edge("refund_tools", "refund")
    
    checkpointer = get_checkpointer()
    graph = workflow.compile(checkpointer=checkpointer)
    
    return graph
