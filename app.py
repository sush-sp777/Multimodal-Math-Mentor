import streamlit as st
from agents.graph import build_graph
from utils.ocr import extract_text_from_image
from utils.asr import transcribe_audio
from PIL import Image
from memory.memory_store import save_to_memory

st.set_page_config(page_title="AI Math Mentor", layout="centered")

st.title("🧮 AI Math Mentor")
st.caption("JEE-style Math Solver using RAG + Agents + HITL")

graph = build_graph()

if "state" not in st.session_state:
    st.session_state.state = None

if "correction_text" not in st.session_state:
    st.session_state.correction_text = ""

if "hitl_approved" not in st.session_state:
    st.session_state.hitl_approved = False

if "hitl_question" not in st.session_state:
    st.session_state.hitl_question = ""

if "needs_hitl" not in st.session_state:
    st.session_state.needs_hitl = False

#input mode
input_mode = st.radio(
    "Select input mode",
    ["Text", "Image", "Audio"],
    horizontal=True
)

question = None

#text input
if input_mode == "Text":
    question = st.text_area("Enter your math question", height=120, placeholder="Type your question here...")

#image input
elif input_mode == "Image":
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_column_width=True)

        ocr = extract_text_from_image(image)
        question = st.text_area("Review OCR text", value=ocr["text"], height=150)
        st.metric("OCR Confidence", ocr["confidence"])

        if ocr["needs_clarification"]:
            st.session_state.needs_hitl = True
            st.warning("Low OCR confidence — please verify")

#audio input
elif input_mode == "Audio":
    audio_file = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "m4a"]
    )

    if audio_file:
        st.audio(audio_file)
        asr = transcribe_audio(audio_file)
        question = st.text_area("Review transcription", value=asr["text"], height=150)
        st.metric("ASR Confidence", asr["confidence"])

        if asr["needs_clarification"]:
            st.session_state.needs_hitl = True
            st.warning("Low transcription confidence — please verify")

# Reset HITL on new input
if question and question != st.session_state.hitl_question:
    st.session_state.hitl_approved = False
    st.session_state.hitl_question = question
    st.session_state.needs_hitl = False

#solve
if question:
    current_verdict = (st.session_state.state or {}).get("verdict", {})
    hitl_needed = st.session_state.needs_hitl or current_verdict.get("status") == "hitl"

    #hitl flow
    if hitl_needed and not st.session_state.hitl_approved:
        st.warning("⚠️ Human-in-the-loop required before solving")

        # Show reason
        hitl_reason = current_verdict.get("reason")
        if hitl_reason:
            st.info(f"Reason for HITL: {hitl_reason}")
        elif st.session_state.needs_hitl:
            st.info("HITL triggered due to low-confidence or ambiguous input.")

        st.markdown("**Please review or correct the question below. Only after approval, the system will solve it.**")

        # Editable HITL question box
        st.session_state.hitl_question = st.text_area(
            "Review / correct the question",
            value=st.session_state.hitl_question,
            height=150
        )

        if st.button("✅ Approve & Continue"):
            st.session_state.hitl_approved = True
            st.session_state.needs_hitl = False
            with st.spinner("Thinking..."):
                try:
                    st.session_state.state = graph.invoke({"question": st.session_state.hitl_question})
                    st.success("✅ Question approved. Solution generated!")
                except Exception as e:
                    st.error(f"Error during solving: {str(e)}")

    #normal solve flow
    elif st.button("🚀 Solve"):
        with st.spinner("Thinking..."):
            st.session_state.state = graph.invoke({"question": question})

state = st.session_state.state

#output
if state:
    st.subheader("🧠 Parsed Problem")
    st.json(state.get("parsed_problem"))

    st.subheader("📚 Retrieved Context")
    context_docs = state.get("context_docs", [])

    if not context_docs:
        st.info("No external context retrieved for this problem.")
    else:
        for i, doc in enumerate(context_docs):
            with st.expander(f"Source {i+1}"):
                st.write(doc.page_content)
                
    with st.expander("🧩 Agent Trace"):
       trace = state.get("trace", [])
       st.text("\n".join(trace))

    verdict = state.get("verdict", {})

    #final ans
    if verdict.get("status") == "hitl":
        st.info("Waiting for human approval or clarification. Please correct the question above to continue.")
    else:
        st.subheader("✅ Final Answer")
        st.markdown(state.get('final_output'))


        conf = state.get("confidence")
        if conf is not None:
            st.metric("Confidence", conf)

        st.divider()
        st.subheader("🧪 Was this solution correct?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Correct"):
                save_to_memory(state, "approved")
                st.success("Saved to memory ✔")

        with col2:
            st.text_area("Correction / feedback", key="correction_text")
            if st.button("❌ Submit Correction"):
                save_to_memory(state, st.session_state.correction_text)
                st.success("Correction saved ✔")
