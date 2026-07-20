import os
import pymysql

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from prompts import (
    SQL_PROMPT,
    ROUTER_PROMPT,
    RAG_PROMPT
)

load_dotenv()


# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# Database Connection
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )


# Load Vector Database
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(
    search_kwargs={"k":3}
)


# SQL Chain
def generate_sql(question):
    sql_chain = (
        SQL_PROMPT
        | llm
        | StrOutputParser()
    )
    sql_query = sql_chain.invoke(
        {
            "question": question
        }
    )

    # Remove markdown code blocks
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()

    return sql_query

def execute_sql(sql_query):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return columns, rows
    except Exception as e:
        print(f"SQL Error: {e}")
        return None, None
    finally:
        if connection:
            connection.close()

def format_sql_result(columns, rows):
    if not rows:
        return "No data found."
    table = ""
    table += " | ".join(columns)
    table += "\n"
    table += "-" * 50
    table += "\n"
    for row in rows:
        table += " | ".join(
            str(value)
            for value in row
        )
        table += "\n"
    return table

def summarize_sql(question, table):
    prompt = f"""
The user asked:
{question}
The database returned:
{table}
Explain this in simple business English.
Keep the answer under 3 sentences.
"""
    response = llm.invoke(prompt)
    return response.content

def run_sql_chain(question):
    sql_query = generate_sql(question)
    print("\nGenerated SQL:\n")
    print(sql_query)
    columns, rows = execute_sql(sql_query)
    if columns is None:
        return (
            "Sorry, I couldn't execute the SQL query. "
            "Please try asking the question differently."
        )
    table = format_sql_result(columns, rows)
    answer = summarize_sql(question, table)
    return answer


# RAG Chain
def retrieve_context(question):
    documents = retriever.invoke(question)
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )
    return context

def generate_rag_answer(question):
    try:
        context = retrieve_context(question)
        if not context.strip():
            return (
                "I couldn't find any relevant information "
                "in the knowledge base."
            )
        rag_chain = (
            RAG_PROMPT
            | llm
            | StrOutputParser()
        )
        answer = rag_chain.invoke({
            "context": context,
            "question": question
        })
        return answer
    
    except Exception as e:
        print(f"RAG Error: {e}")
        return (
            "Sorry, something went wrong while searching "
            "the documents."
        )


# Router
def classify_question(question):
    router_chain = (
        ROUTER_PROMPT
        | llm
        | StrOutputParser()
    )
    route = router_chain.invoke(
        {
            "question": question
        }
    )
    return route.strip().upper()


# Main Chatbot
def answer_question(question):
    try:
        route = classify_question(question)
        print(f"\nRoute Selected : {route}")

        if route == "SQL":
            return run_sql_chain(question)
        elif route == "RAG":
            return generate_rag_answer(question)
        else:
            return (
                "I couldn't determine how to process "
                "your question."
            )
        
    except Exception as e:
        print(f"Application Error: {e}")
        return (
            "Sorry, an unexpected error occurred. "
            "Please try again."
        )

