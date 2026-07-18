import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Agent Settings")
        

        
        # Chunking Strategy
        chunking = st.selectbox(
            "Chunking Strategy",
            options=["character", "semantic", "parent_child"],
            index=["character", "semantic", "parent_child"].index(os.getenv("CHUNKING_STRATEGY", "character"))
        )
        
        # Reranker
        reranker = st.selectbox(
            "Reranker",
            options=["cohere", "local"],
            index=0 if os.getenv("RERANK_PROVIDER", "cohere") == "cohere" else 1
        )
        
        st.divider()
        
        # Memory Panel
        st.header("🧠 Memory")
        if st.session_state.get("long_term_memory_active"):
            st.success("Recalled from past conversations!")
            
        if st.session_state.get("short_term_memory_triggered"):
            st.info("Short-term summarization active this session.")
            
        if st.button("Reset Conversation"):
            import uuid
            st.session_state.thread_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.long_term_memory_active = False
            st.session_state.short_term_memory_triggered = False
            st.rerun()
            
        st.divider()
        

        if st.session_state.get("role") == "admin":
            with st.expander("🛠️ Admin: View Support Tickets"):
                try:
                    import sqlite3
                    import sys
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                    from config.settings import SQLITE_DB_PATH
                    
                    conn = sqlite3.connect(SQLITE_DB_PATH)
                    conn.row_factory = sqlite3.Row
                    c = conn.cursor()
                    c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
                    rows = c.fetchall()
                    if rows:
                        data = [dict(row) for row in rows]
                        st.dataframe(data, hide_index=True)
                    else:
                        st.write("No support tickets yet.")
                    conn.close()
                except Exception as e:
                    st.error("Database not initialized yet.")
                
        st.divider()
        
        # Trace Expander
        with st.expander("Show Agent Reasoning Trace"):
            if st.session_state.get("last_trace"):
                for trace_item in st.session_state.last_trace:
                    st.write(trace_item)
            else:
                st.write("No trace available yet.")
                
        if os.getenv("LANGCHAIN_TRACING_V2") == "true":
            st.caption("Full trace available in LangSmith")
            
        st.divider()
        st.subheader("Sample Questions")
        if st.button("Where is my order #1042?"):
            st.session_state.demo_query = "Where is my order #1042?"
            st.rerun()
        if st.button("What's your return policy?"):
            st.session_state.demo_query = "What's your return policy?"
            st.rerun()
        if st.button("I am very angry, I want a refund NOW"):
            st.session_state.demo_query = "I am very angry, I want a refund NOW"
            st.rerun()
            
        st.divider()
        st.caption("Demo project — all data is synthetic. No real customer information is used.")
