from langgraph.graph import StateGraph
from agents.parser_agent import parse_question
from agents.router_agent import route
from agents.retriever_agent import retrieve
from agents.solver_agent import solve
from agents.verifier_agent import verify
from agents.explainer_agent import explain

def hitl_node(state: dict) -> dict:
    state["verdict"] = {
        "status": "hitl",
        "reason": "Ambiguous or low-confidence input requires human verification"
    }
    state["trace"].append("HITL: graph execution stopped")
    return state

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("parser", parse_question)
    graph.add_node("retriever", retrieve)
    graph.add_node("solver", solve)
    graph.add_node("verifier", verify)
    graph.add_node("explainer", explain)
    graph.add_node("hitl", hitl_node)

    graph.set_entry_point("parser")

    def router_with_trace(state):
        next_node = route(state["parsed_problem"])
        state["trace"].append(f"RouterAgent: routed to {next_node}")
        return next_node

    graph.add_conditional_edges(
        "parser",
        router_with_trace,
        {
            "solve": "retriever",
            "explainer": "explainer",
            "hitl": "hitl"
        }
    )

    graph.add_edge("retriever", "solver")
    graph.add_edge("solver", "verifier")
    graph.add_edge("verifier", "explainer")

    graph.set_finish_point("explainer")
    graph.set_finish_point("hitl")

    return graph.compile()
