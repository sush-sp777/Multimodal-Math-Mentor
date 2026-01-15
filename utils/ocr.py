import easyocr
import numpy as np
from PIL import Image
import streamlit as st

@st.cache_resource(show_spinner="Loading OCR model...")
def load_ocr_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_ocr_reader()

def extract_text_from_image(image) -> dict:
    """
    Returns:
    {
        "text": extracted_text,
        "confidence": avg_confidence,
        "needs_clarification": bool
    }
    """

    img = np.array(image)

    results = reader.readtext(img)

    extracted_text = []
    confidences = []

    for bbox, text, conf in results:
        extracted_text.append(text)
        confidences.append(conf)

    final_text = " ".join(extracted_text)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return {
        "text": final_text,
        "confidence": round(avg_confidence, 2),
        "needs_clarification": avg_confidence < 0.6
    }
