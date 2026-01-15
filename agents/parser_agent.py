def parse_question(state: dict) -> dict:
    state.setdefault("trace", []).append("ParserAgent: started parsing input")

    question = state["question"]
    clean_question = question.strip()

    needs_clarification = False
    if len(clean_question.split()) < 3:
        needs_clarification = True

    topic = "general"
    text_lower = clean_question.lower()

    if "probability" in text_lower or "dice" in text_lower:
        topic = "probability"
    elif "derivative" in text_lower or "limit" in text_lower:
        topic = "calculus"
    elif "matrix" in text_lower or "determinant" in text_lower:
        topic = "linear_algebra"
    elif "x" in text_lower or "equation" in text_lower:
        topic = "algebra"

    state["parsed_problem"] = {
        "problem_text": clean_question,
        "topic": topic,
        "needs_clarification": needs_clarification
    }

    state["trace"].append(
        f"ParserAgent: topic={topic}, needs_clarification={needs_clarification}"
    )

    return state
