def route(parsed_problem: dict) -> str:
    """
    Intent Router Agent
    Routes to the appropriate agent based on topic or need for HITL
    """

    # First, check if clarification is needed
    if parsed_problem.get("needs_clarification", False):
        return "hitl"

    # Route based on topic
    topic = parsed_problem.get("topic", "general").lower()

    if topic in ["algebra", "linear_algebra", "calculus", "probability"]:
        return "solve"

    # If user asks for explanation
    text = parsed_problem.get("problem_text", "").lower()
    if "explain" in text or "why" in text:
        return "explainer"

    return "solve"
