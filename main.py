# ============================
# main.py — ToxiGuard AI (Premium UI)
# ============================

import streamlit as st
import joblib
import re
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
from utils.abuse_words import abusive_words, suggestions, detect_abusive_tokens

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="ToxiGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- PREMIUM GLOBAL CSS ----------------
st.markdown("""
<style>

/* ===== Root Background ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 60%, #020617 100%);
    color: #e5e7eb;
}

/* ===== Remove White Header ===== */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #020617, #0f172a);
    box-shadow: 0 4px 25px rgba(0,0,0,0.6);
}
header[data-testid="stHeader"] * {
    color: #e5e7eb !important;
}

/* ===== Remove White Decorations ===== */
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    background: transparent !important;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* ===== Glass Cards ===== */
.glass {
    background: rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 24px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 0 40px rgba(56,189,248,0.15);
}

/* ===== Text Area ===== */
textarea {
    background: rgba(2,6,23,0.9) !important;
    color: #f9fafb !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
textarea::placeholder {
    color: #94a3b8 !important;
}

/* ===== Buttons ===== */
.stButton>button {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: #020617 !important;
    font-weight: 800;
    border-radius: 999px;
    padding: 0.65em 2.6em;
    border: none;
    box-shadow: 0 0 25px rgba(56,189,248,0.5);
    transition: all 0.25s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(99,102,241,0.8);
}

/* ===== KPI Cards ===== */
.kpi-card {
    background: linear-gradient(
        160deg,
        rgba(56,189,248,0.18),
        rgba(99,102,241,0.18)
    );
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    color: #f9fafb !important;
    box-shadow: 0 0 35px rgba(56,189,248,0.3);
}
.kpi-card h2 {
    margin: 6px 0;
    color: #ffffff !important;
}

/* ===== Expanders ===== */
details, summary {
    background: rgba(255,255,255,0.12) !important;
    border-radius: 16px;
    padding: 6px;
}

/* ===== Highlight Abusive Words ===== */
.abusive-word {
    background: linear-gradient(135deg, #ef4444, #f97316);
    color: #ffffff;
    padding: 2px 8px;
    border-radius: 8px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NLTK ----------------
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# ---------------- Load Model ----------------
pipeline = joblib.load("abuse_model.joblib")

# ---------------- Utils ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+|#\w+", " ", text)
    text = re.sub(r"[^a-z0-9\s\*]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def normalize_censored(text):
    text = re.sub(r"f\*+k", "fuck", text, flags=re.I)
    text = re.sub(r"a\*+hole", "asshole", text, flags=re.I)
    return text

def analyze_text(text):
    text = normalize_censored(text)
    cleaned = clean_text(text)
    pred = pipeline.predict([cleaned])[0]
    prob = pipeline.predict_proba([cleaned])[0][1]
    abusive_tokens = detect_abusive_tokens(text)
    polarity = TextBlob(text).sentiment.polarity
    sentiment = "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"
    return cleaned, pred, prob, abusive_tokens, sentiment, polarity

# ---------------- Header ----------------
st.markdown("""
<h1 style="
text-align:center;
font-size:3rem;
color:#38bdf8;
text-shadow:0 0 20px rgba(56,189,248,0.7);
">
🛡️ ToxiGuard AI
</h1>

<p style="text-align:center;color:#e5e7eb;font-size:1.1rem;">
Real-time Abuse Detection • Sentiment Analysis • NLP Insights
</p>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("<h2>⚙️ Control Panel</h2>", unsafe_allow_html=True)
real_time = st.sidebar.toggle("⚡ Real-Time Analysis", value=False)

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar.expander("📜 Search History", expanded=True):
    for i, t in enumerate(reversed(st.session_state.history[-15:]), 1):
        st.write(f"{i}. {t}")

# ---------------- Input ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#38bdf8;'>✍️ Enter text for analysis</h4>", unsafe_allow_html=True)

user_input = st.text_area("", height=160, placeholder="Type or paste text here...")
st.markdown("</div>", unsafe_allow_html=True)

analyze_clicked = st.button("🔍 Analyze Sentence")

# ---------------- Analysis ----------------
def run_analysis(text):
    cleaned, pred, prob, abusive_tokens, sentiment, polarity = analyze_text(text)

    total = len(cleaned.split())
    abusive = len(abusive_tokens)
    clean = total - abusive

    st.markdown(f"""
    <div style="display:flex;gap:20px;margin-top:20px;">
        <div class="kpi-card">📄 Total Words<br><h2>{total}</h2></div>
        <div class="kpi-card">⚠️ Abusive<br><h2>{abusive}</h2></div>
        <div class="kpi-card">✅ Clean<br><h2>{clean}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    highlighted = text
    for w in abusive_tokens:
        highlighted = re.sub(
            f"(?i){re.escape(w)}",
            f"<span class='abusive-word'>{w}</span>",
            highlighted
        )

    st.markdown(f"<div class='glass'><b>Sentence:</b><br>{highlighted}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass" style="margin-top:15px;">
    <b>Prediction:</b> {'⚠️ ABUSIVE' if pred else '✅ CLEAN'}<br>
    Sentiment: <b>{sentiment}</b> (Polarity {polarity:.2f})<br>
    Confidence: <b>{prob:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({"Type": ["Abusive", "Clean"], "Count": [abusive, clean]})
    fig = px.pie(df, names="Type", values="Count",
                 color="Type",
                 color_discrete_map={"Abusive": "#ef4444", "Clean": "#22c55e"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Trigger ----------------
if user_input.strip():
    if user_input not in st.session_state.history:
        st.session_state.history.append(user_input)
    if analyze_clicked or real_time:
        run_analysis(user_input)

# ---------------- Footer ----------------
st.markdown("""
<hr>
<p style="text-align:center;color:#94a3b8;">
Powered by <b>ToxiGuard AI</b> • GenAI • NLP • Streamlit
</p>
""", unsafe_allow_html=True)
