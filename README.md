# 🧮 AI Math Mentor

- Multimodal Math Solver using RAG + Agents + HITL + Memory
---
## 📌 Overview

AI Math Mentor is an end-to-end multimodal AI application designed to solve JEE-level math problems reliably.
It supports text, image, and audio inputs, explains solutions step-by-step, verifies correctness, and improves over time using human feedback and memory.

This project demonstrates:

- RAG (Retrieval-Augmented Generation)
- Multi-agent orchestration
- Human-in-the-loop (HITL)
- Runtime memory & learning signals
- A deployable Streamlit application
---
## 🎯 Objectives 

This project satisfies all mandatory requirements of the AI Engineer Assignment:

- ✅ Multimodal input (Text / Image / Audio)
- ✅ OCR & ASR with user verification
- ✅ Parser Agent with ambiguity detection
- ✅ RAG pipeline using FAISS
- ✅ Multi-agent system (Parser, Router, Solver, Verifier, Explainer)
- ✅ Human-in-the-Loop (HITL)
- ✅ Memory & self-learning (pattern reuse)
- ✅ Streamlit UI
- ✅ Deployment-ready design
---
## 📐 Supported Math Scope

- Algebra
- Probability
- Basic Calculus (limits, derivatives, simple optimization)

## 🧠 System Architecture
```
User Input (Text / Image / Audio)
        ↓
OCR / ASR (EasyOCR / Whisper)
        ↓
Parser Agent
(cleaning + topic detection + ambiguity check)
        ↓
Intent Router Agent
        ↓
RAG Retriever (FAISS)
        ↓
Solver Agent (LLM + context)
        ↓
Verifier Agent (confidence & correctness check)
        ↓
Explainer Agent (step-by-step solution)
        ↓
User Feedback → Memory (FAISS)
```
---
## 🤖 Agents Overview
1️⃣ Parser Agent

- Cleans OCR / ASR output
- Detects ambiguity or missing info
- Extracts:
```json
{
  "problem_text": "...",
  "topic": "calculus",
  "needs_clarification": false
}
```
- Triggers HITL if needed

2️⃣ Intent Router Agent

- Routes flow based on parsed problem
- Uses deterministic logic 
- Routes to:
solve
explain
hitl

3️⃣ Retriever Agent (RAG)

- Retrieves relevant math knowledge:
formulas
identities
solution templates
- Uses FAISS vector store
- Displays retrieved sources in UI

4️⃣ Solver Agent

- Solves problems using:
LLM
Retrieved RAG context
- Produces:
raw reasoning
final answer

5️⃣ Verifier Agent

Checks:
- empty or invalid answers
- uncertainty language
- missing final result
- Approves or triggers HITL
- Assigns confidence score

6️⃣ Explainer Agent

- Converts solution into student-friendly explanation
- Uses proper math formatting:

x², x³, √(x + 1)

- Produces final output shown to user
---

## 🧑‍⚖️ Human-in-the-Loop (HITL)

HITL is triggered when:
- OCR / ASR confidence is low
- Parser detects ambiguity
- Verifier is unsure
- User corrects the question
HITL flow:
- User reviews / edits extracted question
- Clicks Approve & Continue
- Approved input is solved
- Feedback stored as learning signal

--- 

## 🧠 Memory & Self-Learning

- What is stored
- Original input
- Parsed question
- Retrieved context
- Final answer
- Verifier outcome
- User feedback (correct / correction)
- How memory is used
- Retrieves similar past problems
- Reuses solution patterns
- Applies known correction patterns
---

## 🔧 Setup Instructions
1️⃣ Clone repository
```
git clone https://github.com/sush-sp777/Multimodal-Math-Mentor
cd Multimodal-Math-Mentor
```
2️⃣ Create virtual environment
```
python -m venv venv
source venv/bin/activate
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
3️⃣ Install dependencies
create .env:
```
GROQ_API_KEY=your_api_key_here
```
5️⃣ Run app
```
streamlit run app.py
```
---
## 👨‍💻 Author

**Sushant Patil**

Generative AI Engineer

🔗 https://github.com/sush-sp777
🔗 https://www.linkedin.com/in/sushant-patil-9a05ab2a4/

---

