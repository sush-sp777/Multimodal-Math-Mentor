from rag.retriever import retrieve_context
from memory.memory_store import retrieve_from_memory

def retrieve(state: dict) -> dict:
    state.setdefault("trace", []).append("RetrieverAgent: started retrieval")

    query = state["parsed_problem"]["problem_text"]

    #retrieve memory first
    memory_docs = retrieve_from_memory(query)
    rag_docs = retrieve_context(query)

    #memory gets priority
    combined_docs = []

    for doc in memory_docs:
        doc.metadata["type"] = "memory"
        combined_docs.append(doc)

    for doc in rag_docs:
        doc.metadata["type"] = "rag"
        combined_docs.append(doc)

    state["context_docs"] = combined_docs

    state["trace"].append(
        f"RetrieverAgent: memory_docs={len(memory_docs)}, rag_docs={len(rag_docs)}"
    )

    return state
