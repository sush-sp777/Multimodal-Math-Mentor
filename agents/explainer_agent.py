# agents/explainer_agent.py
import re

SUPERSCRIPTS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def format_math_friendly(text: str) -> str:
    """
    Convert solver output to student-friendly math:
    - x^n or x^{n} → xⁿ
    - y^n or y^{n} → yⁿ
    - \sqrt{expr} → √expr
    - Replace EN DASH with normal minus
    """
    text = text.replace("–", "-") 

    text = re.sub(r"([xy])\^\{?(\d+)\}?", lambda m: m.group(1) + m.group(2).translate(SUPERSCRIPTS), text)

    text = re.sub(r"\\sqrt\{([^}]+)\}", r"√\1", text)

    return text

def explain(state: dict) -> dict:
    state.setdefault("trace", []).append("ExplainerAgent: preparing explanation")

    solution = state.get("solution", {})
    explanation = solution.get("raw_answer") or solution.get("final_answer") or "No solution available"

    state["final_output"] = format_math_friendly(explanation)

    state["trace"].append("ExplainerAgent: explanation delivered")
    return state
