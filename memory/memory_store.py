import os
import json
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_PATH = os.path.join(BASE_DIR, "memory", "faiss_index")
JSON_LOG_PATH = os.path.join(BASE_DIR, "memory", "memory_log.json")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
#load faiss
def load_memory():
    if os.path.exists(MEMORY_PATH):
        return FAISS.load_local(
            MEMORY_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return None

#save json
def save_json(entry: dict):
    data = []

    if os.path.exists(JSON_LOG_PATH):
        try:
            with open(JSON_LOG_PATH, "r") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            data = []

    data.append(entry)

    with open(JSON_LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

#save to memory
def save_to_memory(state: dict, feedback: str):
    vectorstore = load_memory()

    parsed = state.get("parsed_problem", {})
    solution = state.get("solution", {})

    memory_text = f"""
    Topic: {parsed.get('topic')}
    Problem Pattern: {parsed.get('problem_text')}
    Correct Answer: {solution.get('answer')}
    Human Feedback: {feedback}

    Instruction:
    For similar problems, follow the corrected reasoning and explanation style.
    """

    doc = Document(
        page_content=memory_text.strip(),
        metadata={
            "topic": parsed.get("topic"),
            "confidence": solution.get("confidence"),
            "source": "human_feedback"
        }
    )

    if vectorstore is None:
        vectorstore = FAISS.from_documents([doc], embeddings)
    else:
        vectorstore.add_documents([doc])

    vectorstore.save_local(MEMORY_PATH)

    save_json({
        "timestamp": datetime.utcnow().isoformat(),
        "topic": parsed.get("topic"),
        "problem": parsed.get("problem_text"),
        "answer": solution.get("answer"),
        "feedback": feedback
    })

#retrieve
def retrieve_from_memory(query: str, k: int = 2):
    vectorstore = load_memory()
    if vectorstore is None:
        return []
    return vectorstore.similarity_search(query, k=k)
