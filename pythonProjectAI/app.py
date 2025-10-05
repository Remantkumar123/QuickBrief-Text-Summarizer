import streamlit as st
from transformers import pipeline
import base64

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="QuickBrief ", page_icon="🧠", layout="centered")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #74ABE2, #5563DE);
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-top: 40px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        }
        textarea, .stTextInput>div>div>input {
            background-color: rgba(255,255,255,0.8) !important;
            color: #000 !important;
            border-radius: 10px !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #6a11cb, #2575fc);
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #fff;
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown("<h1 style='text-align:center; color:white; font-size:28px;'>🧠 QuickBrief Less Reading More Knowing</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Summarize long paragraphs into short, meaningful summaries in seconds.</p>", unsafe_allow_html=True)

# ------------------- TEXT INPUT -------------------
input_text = st.text_area("✍️ Enter your text below:", height=200, placeholder="Paste or type your paragraph here...")

# ------------------- LOAD MODEL -------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# ------------------- SUMMARIZE BUTTON -------------------
if st.button("✨ Generate Summary"):
    if input_text.strip():
        with st.spinner("⏳ AI is summarizing your text..."):
            summary = summarizer(input_text, max_length=150, min_length=40, do_sample=False)
            result = summary[0]['summary_text']

        st.subheader("📝 Summary:")
        st.success(result)

        # Copy to clipboard
        st.markdown(f"""
            <button onclick="navigator.clipboard.writeText('{result}')"
            style="margin-top:10px;background:#4CAF50;color:white;padding:10px;border:none;border-radius:10px;cursor:pointer;">
            📋 Copy Summary
            </button>
        """, unsafe_allow_html=True)

        # Download button
        b64 = base64.b64encode(result.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="summary.txt">📥 Download as .txt</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter some text to summarize!")

# ------------------- FOOTER -------------------
st.markdown("<div class='footer'>QuickBrief — because every second you save brings you closer to understanding more.</div>", unsafe_allow_html=True)
