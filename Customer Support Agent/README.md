# NovaShop AI Support Supervisor

A full-stack, AI-powered customer support application built using LangGraph, Streamlit, SQLite, and Qdrant. This architecture features role-based access control, persistent long-term memory, dynamic identity injection, and specialized autonomous agents (FAQ, Order Management, and Refund Processing).

## 🚀 Architecture Overview

This project is not a simple chatbot; it is a multi-agent orchestrated system:
- **Streamlit Frontend**: A secure, session-based UI with User and Admin roles.
- **State Manager**: Dynamically tracks chat history and securely injects the user's authenticated identity natively into the LLM state.
- **LangGraph Supervisor**: Analyzes semantic intent and dynamically routes the user to the correct specialized worker agent.
- **FAQ Agent**: Uses Hybrid Search RAG (Vector Embeddings + BM25) to answer policy questions using Qdrant.
- **Order & Refund Agents**: Use LangChain Tool Calling to execute raw, exact-match SQL queries against an SQLite database.
- **Checkpointer Memory**: Serializes the absolute graph state to SQLite, allowing users to log out and return days later with perfect memory retention.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:
- **Python 3.10+**
- **Git** (if cloning from a repository)

You will also need an API key for your LLM provider (e.g., Groq, OpenAI, or Anthropic).

---

## 💻 Step-by-Step Installation

### 1. Clone the Repository
Download or clone the project folder to your local machine, and navigate into it using your terminal:
```bash
git clone <repository_url>
cd "Customer Support Agent"
```

### 2. Set Up a Virtual Environment (Recommended)
It is best practice to isolate your dependencies using a virtual environment.
```bash
# Windows
python -m venv new
new\Scripts\activate

# macOS/Linux
python3 -m venv new
source new/bin/activate
```

### 3. Install Dependencies
Install all required Python packages via pip:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory (where `app.py` is located) and add your API keys. For example, if you are using Groq:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: If you are using a different LLM provider, update the `llm/model_factory.py` file to point to your respective provider).*

---

## ⚙️ Initializing the Databases

Before launching the app, you must initialize both the SQL relational database and the Vector document database.

### 1. Initialize the SQLite Database
Run the setup script to generate the mock relational database (`novashop.db`). This contains the mock users, orders, and refund eligibility logic.
```bash
python database/db_setup.py
```

### 2. Ingest FAQ Documents to Qdrant
Run the ingestion script to process your company policy documents, generate embeddings, and load them into the local Qdrant vector database.
```bash
python ingestion/load_documents.py
```

---

## ▶️ Running the Application

Once the databases are populated, you are ready to start the Streamlit server!

```bash
streamlit run app.py
```

A browser window will automatically open pointing to `http://localhost:8501`.

---

## 🧪 Testing the Application (Demo Credentials)

The system enforces strict Role-Based Access Control (RBAC). Use the following demo credentials to log in and test different perspectives:

**Customer Account 1 (Leslie):**
- **Username:** `leslie`
- **Password:** `password`
- *Try asking:* "Where is my order #1042?" or "Do you know my name?"

**Customer Account 2 (Allison):**
- **Username:** `allison`
- **Password:** `password`
- *Try asking:* "I want a refund for order #1043."

**Admin Account:**
- **Username:** `admin`
- **Password:** `adminpass`
- *Try:* Asking backend policy questions or reviewing global database queries.

## 📁 Key File Structure
- `app.py`: The Streamlit frontend and session state manager.
- `graph/build_graph.py`: The core LangGraph compilation logic and supervisor routing.
- `graph/agents.py`: The specialized worker prompts and tool bindings.
- `graph/state_schema.py`: The shared memory structure (with `add_messages` deduplication).
- `database/db_queries.py`: The exact-match Python functions executing SQL queries for the agents.
- `embeddings/embedding_service.py`: The HuggingFace integration for the hybrid RAG architecture.
- `Architecture.html`: Open this file in a browser to see an interactive visualization of the system!
