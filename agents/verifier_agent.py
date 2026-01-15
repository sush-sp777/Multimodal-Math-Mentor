def verify(state: dict) -> dict:
    state.setdefault("trace", []).append("VerifierAgent: started verification")

    solution = state.get("solution", {})
    raw_answer = solution.get("raw_answer", "")
    final_answer = solution.get("final_answer", "")
    confidence = state.get("confidence", 0.8)  

    if not raw_answer or "no solution" in raw_answer.lower():
        state["verdict"] = {
            "status": "hitl",
            "reason": "Empty or invalid solution"
        }
        state["trace"].append("VerifierAgent: rejected (empty solution)")
        return state

    if not final_answer:
        state["verdict"] = {
            "status": "hitl",
            "reason": "Final answer missing"
        }
        state["trace"].append("VerifierAgent: rejected (missing final answer)")
        return state

    red_flags = ["maybe", "guess", "not sure", "approximately"]
    if any(flag in raw_answer.lower() for flag in red_flags):
        state["verdict"] = {
            "status": "hitl",
            "reason": "Uncertain language detected"
        }
        state["trace"].append("VerifierAgent: uncertainty detected")
        return state

    state["verdict"] = {
        "status": "approved"
    }

    state["confidence"] = round(min(confidence, 0.95), 2)

    state["trace"].append("VerifierAgent: solution approved")
    return state
