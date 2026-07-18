# Lab Manual: Building the NovaShop AI Agent From Scratch

It will take you step-by-step through the process of building the NovaShop AI Support Agent completely from scratch. 

By following this guide, you will learn how to create your own dummy datasets, orchestrate a multi-agent AI system, and deploy it to a web browser.

---

## Step 1: Environment Setup
Before writing any code, we need to set up a clean Python environment and install the required AI libraries.

1. Create a new project folder and open your terminal.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   ```
3. Install the core dependencies required for LangGraph, Streamlit, and Qdrant:
   ```bash
   pip install streamlit langgraph langchain-core langchain-groq qdrant-client sentence-transformers rank-bm25
   ```
4. Get a free API key from [Groq](https://console.groq.com/) and save it to a `.env` file in your project root:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```

---

## Step 2: Creating the Sample Datasets
An AI is only as good as its data. We need to create two types of data: **Structured** (SQL) and **Unstructured** (Text).

### 2.1 Structured Data (SQLite)
Instead of manually typing SQL commands, we create a Python script to generate a dummy database for our AI to query.
1. Create a file called `database/setup_db.py`.
2. Write a script that uses Python's built-in `sqlite3` library to create three tables: `Customers`, `Orders`, and `Refunds`.
3. Insert some fake data (e.g., John Doe, Order #123, Shipped).
4. **Run the script:** `python database/setup_db.py`. This generates a physical `novashop.db` file in your project.

### 2.2 Unstructured Data (Markdown)
To teach the AI about company policies, we use raw text files.
1. Create a folder called `data/raw/faq_docs/`.
2. Inside, create a file called `company_policy.md`.
3. Write out fake policies regarding shipping, returns, and warranties (e.g., *"Returns are accepted within 30 days"*).

---

## Step 3: Data Ingestion (Vector Database)
The AI cannot read Markdown files instantly; it needs them converted into mathematical vectors.

1. Create a file called `ingestion/load_documents.py`.
2. Write a script that reads `company_policy.md` and splits it into smaller chunks (paragraphs).
3. Use `SentenceTransformers` to convert the text into **Dense Vectors** (384-dimensional numbers).
4. Save these vectors into a local **Qdrant** database, and save a keyword-based version into a **BM25** sparse index.
5. **Run the script:** `python ingestion/load_documents.py`. Your Vector DB is now populated!

---

## Step 4: Building the AI Tools
Now we need to give our AI the ability to physically interact with the SQLite database we built in Step 2.

1. Create a file called `tools/sql_tools.py`.
2. Write a Python function called `check_order_status(customer_id, order_id)`.
3. Add the Langchain `@tool` decorator above the function. This decorator magically exposes the function to the LLM, allowing the AI to pass parameters into it.
4. The function should execute a `SELECT` statement against `novashop.db` and return the raw JSON rows.

---

## Step 5: Orchestrating with LangGraph (The Brain)
This is where the magic happens. We will build a Multi-Agent system where a "Manager" delegates tasks to "Workers".

1. Create `graph/state_schema.py`. Define an `AgentState` object that holds the chat history and the user's `customer_id`.
2. Create `graph/nodes/supervisor.py`. Write a prompt instructing the LLM: *"You are a router. Read the user's message and output only 'faq', 'order', or 'refund'."*
3. Create `graph/nodes/order_agent.py`. Write a prompt instructing this LLM to use the `@tool` from Step 4 to answer the user's question.
4. Create `graph/build_graph.py`. Use LangGraph to physically wire these nodes together:
   ```python
   workflow = StateGraph(AgentState)
   workflow.add_node("Supervisor", supervisor_node)
   workflow.add_node("OrderAgent", order_agent_node)
   
   # Add Conditional Edges based on what the Supervisor decides!
   workflow.add_conditional_edges("Supervisor", lambda state: state["next_node"])
   ```

---

## Step 6: Building the Streamlit UI
Finally, we need a frontend so users can actually chat with the AI!

1. Create `app.py`.
2. Use `st.chat_input()` to create a text box at the bottom of the screen.
3. Use `st.chat_message()` to display the conversation history.
4. When the user types a message, pass it into the LangGraph engine we built in Step 5:
   ```python
   response = st.session_state.graph.stream({"messages": [user_input]})
   ```

---

## Step 7: Running the Project in the Browser!
You have now built a database, ingested vectors, orchestrated a multi-agent AI, and built a frontend!

To bring it all to life, execute the final command in your terminal:
```bash
streamlit run app.py
```

A browser window will automatically open to `http://localhost:8501`. You can now log in and chat with your fully autonomous AI Support Agent!
