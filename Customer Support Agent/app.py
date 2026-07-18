import streamlit as st
import uuid
import sys
import os

sys.path.append(os.path.dirname(__file__))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from graph.build_graph import build_support_graph
from ui.components import render_message
from ui.sidebar import render_sidebar
from memory.memory_manager import manage_short_term_memory

st.set_page_config(page_title="NovaShop AI Support Supervisor", page_icon="🤖")

st.title("NovaShop AI Support Supervisor")

# --- LOGIN SYSTEM ---
USERS = {
    "allison": {"password": "password", "role": "customer", "customer_id": "CUST0001", "name": "Allison Hill"},
    "leslie": {"password": "password", "role": "customer", "customer_id": "CUST0002", "name": "Leslie Johnson"},
    "admin": {"password": "adminpass", "role": "admin", "customer_id": None, "name": "Admin"}
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.session_state.customer_id = user["customer_id"]
            st.session_state.name = user["name"]
            st.session_state.thread_id = f"thread_{username}"
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    # Display Demo Credentials
    st.info("**Demo Accounts:**\n\n- Customer 1: `allison` / `password`\n- Customer 2: `leslie` / `password`\n- Admin: `admin` / `adminpass`")
    st.stop()

# --- MAIN APP ---
st.write(f"Welcome back, **{st.session_state.name}**! ({st.session_state.role.capitalize()})")
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()

if "graph" not in st.session_state:
    st.session_state.graph = build_support_graph()

config = {"configurable": {"thread_id": st.session_state.thread_id}}

if "messages" not in st.session_state:
    # Attempt to pull long-term memory from LangGraph Checkpointer
    state = st.session_state.graph.get_state(config)
    if state and state.values and "messages" in state.values:
        st.session_state.messages = list(state.values["messages"])
    else:
        st.session_state.messages = []

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        render_message("user", msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        render_message("assistant", msg.content)

user_input = st.chat_input("How can I help you today?")
demo_query = st.session_state.pop("demo_query", None)

input_to_process = demo_query or user_input

if input_to_process:
    human_msg = HumanMessage(content=input_to_process)
    st.session_state.messages.append(human_msg)
    render_message("user", input_to_process)
    
    current_messages = manage_short_term_memory(st.session_state.messages)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    
    with st.spinner("Processing..."):
        try:
            traces = []
            final_state = None
            
            # Build Context String dynamically per turn
            context_str = f"USER IDENTITY OVERRIDE: The user's name is {st.session_state.name}."
            if st.session_state.customer_id:
                context_str += f" Their Customer ID is {st.session_state.customer_id}."
            if st.session_state.role == 'admin':
                context_str += " They are a Site Administrator."
            context_str += " You are fully authorized and required to explicitly state their name if they ask for it. Do not ask for confirmation."
                
            for event in st.session_state.graph.stream({"messages": current_messages, "customer_context": context_str}, config=config):
                for node_name, node_state in event.items():
                    traces.append(f"✅ Executed Node: **{node_name}**")
                    messages = node_state.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        if getattr(last_msg, "tool_calls", None):
                            for tc in last_msg.tool_calls:
                                traces.append(f"🛠️ Tool Call: `{tc['name']}`")
                final_state = list(event.values())[0]
            
            st.session_state.last_trace = traces
            
            if final_state:
                final_messages = final_state.get("messages", [])
                if final_messages:
                    last_ai_msg = final_messages[-1]
                    st.session_state.messages.append(last_ai_msg)
                    render_message("assistant", last_ai_msg.content)
        except Exception as e:
            st.error(f"Error processing request: {e}")

# Render the sidebar AFTER processing so it has the latest trace
render_sidebar()
