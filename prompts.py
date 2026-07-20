from langchain_core.prompts import PromptTemplate

# ----------------------------------------------------
# SQL PROMPT
# ----------------------------------------------------

SQL_PROMPT = PromptTemplate.from_template("""
You are an expert MySQL developer.

Convert the user's question into a valid MySQL query.

Database Schema:

customers(
customer_id,
customer_name,
region,
segment
)

products(
product_id,
product_name,
category,
price
)

employees(
employee_id,
employee_name,
department
)

deals(
deal_id,
customer_id,
product_id,
employee_id,
revenue,
status,
close_date
)

tickets(
ticket_id,
customer_id,
issue,
resolved,
created_date
)

Return ONLY SQL.

Question:

{question}

SQL:
""")

# ----------------------------------------------------
# ROUTER PROMPT
# ----------------------------------------------------

ROUTER_PROMPT = PromptTemplate.from_template("""
You are an intelligent routing assistant.

Your task is to classify the user's question into one of two categories.

Return ONLY ONE WORD.

SQL

or

RAG

Choose SQL if the question is about:

customers

sales

revenue

database

count

average

sum

maximum

minimum

employees

products

tickets

price

Choose RAG if the question is about:

refund

policy

pricing

leave

working hours

employee handbook

support

documentation

Question:

{question}
""")

# ----------------------------------------------------
# RAG PROMPT
# ----------------------------------------------------

RAG_PROMPT = PromptTemplate.from_template("""
You are an AI Sales Assistant.

Answer ONLY using the provided context.

If the answer is not present,

say

"I don't have enough information."

Context:

{context}

Question:

{question}

Answer:
""")