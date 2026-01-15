import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import streamlit as st

groq_api_key = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.2
)

def solve(state: dict) -> dict:
    """
    Solver Agent
    - Uses LLM for reasoning
    - Uses RAG context as reference (open book)
    """
    state.setdefault("trace", []).append("SolverAgent: solving using LLM")

    parsed = state["parsed_problem"]
    context_docs = state.get("context_docs", [])

    context_text = ""
    if context_docs:
        context_text = "\n".join(
            [doc.page_content for doc in context_docs]
        )

    prompt = f"""
You are a highly accurate JEE-level Math Mentor.

Use reference material ONLY if relevant:
{context_text}

Rules:
- Be mathematically correct
- Show step-by-step reasoning
- Clearly state the final answer at the end

Problem:
{parsed["problem_text"]}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        answer_text = response.content.strip()

        # Simple heuristic to extract final answer
        final_answer = None
        lines = answer_text.split("\n")
        for line in reversed(lines):
            if "=" in line or "/" in line:
                final_answer = line.strip()
                break

        state["solution"] = {
            "raw_answer": answer_text,
            "final_answer": final_answer,
            "method_used": "auto",
            "steps_complete": True
        }

        state["trace"].append(
            "SolverAgent: solution generated successfully"
        )

    except Exception as e:
        state["solution"] = {
            "raw_answer": f"Error while solving: {str(e)}",
            "final_answer": None,
            "method_used": None,
            "steps_complete": False
        }

        state["trace"].append(
            f"SolverAgent: error occurred - {str(e)}"
        )

    return state
