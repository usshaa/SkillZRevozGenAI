import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import LONG_TERM_STORE_PATH, LONG_TERM_MEMORY_ENABLED

def get_checkpointer():
    if not LONG_TERM_MEMORY_ENABLED:
        return None
        
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        import sqlite3
        
        os.makedirs(os.path.dirname(LONG_TERM_STORE_PATH), exist_ok=True)
        # Create a persistent connection
        conn = sqlite3.connect(LONG_TERM_STORE_PATH, check_same_thread=False)
        # Instantiate the saver with the connection
        checkpointer = SqliteSaver(conn)
        # Call setup to initialize tables
        checkpointer.setup()
        
        return checkpointer
    except Exception as e:
        print(f"Error initializing SQLite Checkpointer: {e}")
        raise
