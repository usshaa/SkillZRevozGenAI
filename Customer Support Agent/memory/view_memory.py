import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Path to the memory database
DB_PATH = "data/memory_store/novashop_memory.db"

def view_memory():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    print("Connecting to the Checkpointer...")
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        checkpointer = SqliteSaver(conn)
        
        # We need a thread_id to look up. Let's list all threads first!
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        threads = cursor.fetchall()
        
        if not threads:
            print("No memory checkpoints found! Try chatting with the AI first.")
            return
            
        print("\nFound the following Thread IDs (User Sessions) in Memory:")
        for t in threads:
            print(f"- {t[0]}")
            
        # Grab the first thread to visualize
        target_thread = threads[0][0]
        config = {"configurable": {"thread_id": target_thread}}
        
        print(f"\n--- Decoded Memory for Thread: {target_thread} ---")
        
        # The Checkpointer automatically decodes the BLOB!
        state = checkpointer.get(config)
        
        if state and "channel_values" in state:
            memory_data = state["channel_values"]
            print(f"\nCustomer Context Injected: {memory_data.get('customer_context')}")
            
            print("\nConversation History:")
            for msg in memory_data.get("messages", []):
                msg_type = type(msg).__name__
                content = msg.content
                print(f"[{msg_type}]: {content[:100]}...") # Truncated for readability
        else:
            print("No data found in state.")

if __name__ == "__main__":
    view_memory()
