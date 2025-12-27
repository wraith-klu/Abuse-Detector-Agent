# ============================
# main.py — ToxiGuard AI (Premium UI)
# ============================

import streamlit as st
import joblib
import re
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

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
    background: radial-gradient(
        circle at top,
        #0f172a 0%,
        #020617 45%,
        #020617 100%
    );
    color: #e5e7eb;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont;
}

/* ===== Remove White Header ===== */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #020617, #0f172a);
    box-shadow: 0 8px 30px rgba(0,0,0,0.75);
    border-bottom: 1px solid rgba(255,255,255,0.06);
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
    box-shadow: inset -10px 0 30px rgba(0,0,0,0.55);
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* ===== Glass Cards ===== */
.glass {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.14),
        rgba(255,255,255,0.04)
    );
    border-radius: 26px;
    padding: 26px;
    backdrop-filter: blur(22px) saturate(140%);
    -webkit-backdrop-filter: blur(22px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.05),
        0 25px 60px rgba(0,0,0,0.55),
        0 0 45px rgba(56,189,248,0.18);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.glass:hover {
    transform: translateY(-3px);
    box-shadow:
        0 35px 80px rgba(0,0,0,0.65),
        0 0 60px rgba(99,102,241,0.45);
}

/* ===== Text Area ===== */
textarea {
    background: rgba(2,6,23,0.94) !important;
    color: #f9fafb !important;
    border-radius: 22px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 16px !important;
    transition: border 0.2s ease, box-shadow 0.2s ease;
}
textarea:focus {
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.35);
}
textarea::placeholder {
    color: #94a3b8 !important;
}

/* ===== Buttons ===== */
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: #020617 !important;
    font-weight: 800;
    letter-spacing: 0.4px;
    border-radius: 999px;
    padding: 0.75em 3em;
    border: none;
    box-shadow:
        0 10px 25px rgba(56,189,248,0.45),
        inset 0 1px 0 rgba(255,255,255,0.35);
    transition: all 0.25s ease;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.06);
    box-shadow:
        0 20px 50px rgba(99,102,241,0.85);
}

/* ===== KPI Cards ===== */
.kpi-card {
    background: linear-gradient(
        160deg,
        rgba(56,189,248,0.25),
        rgba(99,102,241,0.25)
    );
    padding: 26px;
    border-radius: 26px;
    text-align: center;
    color: #f9fafb !important;
    box-shadow:
        0 18px 45px rgba(56,189,248,0.4),
        inset 0 1px 0 rgba(255,255,255,0.3);
}
.kpi-card h2 {
    margin: 8px 0;
    font-size: 2.2rem;
    color: #ffffff !important;
    text-shadow: 0 0 14px rgba(56,189,248,0.65);
}

/* ===== Expanders ===== */
details, summary {
    background: rgba(255,255,255,0.16) !important;
    border-radius: 18px;
    padding: 8px 12px;
}

/* ===== Highlight Abusive Words ===== */
.abusive-word {
    background: linear-gradient(135deg, #ef4444, #f97316);
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 800;
    box-shadow: 0 0 18px rgba(239,68,68,0.75);
}

/* ============================
   ADVANCED UI ENHANCEMENTS
   ============================ */

/* ===== KPI Number Animation ===== */
@keyframes countUp {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.kpi-card h2 {
    animation: countUp 0.6s ease-out;
}

/* ===== Severity Badges ===== */
.severity-low {
    background: linear-gradient(135deg, #22c55e, #4ade80);
    color: #022c22;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 800;
    box-shadow: 0 0 18px rgba(34,197,94,0.6);
}

.severity-medium {
    background: linear-gradient(135deg, #facc15, #fb923c);
    color: #3b1d00;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 800;
    box-shadow: 0 0 20px rgba(251,146,60,0.7);
}

.severity-high {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: #ffffff;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 900;
    box-shadow: 0 0 25px rgba(239,68,68,0.9);
    animation: dangerPulse 1.2s infinite alternate;
}

/* ===== High Severity Pulse ===== */
@keyframes dangerPulse {
    from {
        box-shadow: 0 0 18px rgba(239,68,68,0.7);
    }
    to {
        box-shadow: 0 0 35px rgba(239,68,68,1);
    }
}

/* ===== Toxic Text Glow ===== */
.toxic-text {
    background: rgba(239,68,68,0.12);
    border-left: 4px solid #ef4444;
    padding: 14px 18px;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(239,68,68,0.35);
}

/* ===== Smooth Page Load ===== */
.stApp {
    animation: appFade 0.4s ease-in;
}

@keyframes appFade {
    from {
        opacity: 0;
        transform: scale(0.985);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
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

def toxicity_level(prob, abusive_count):
    if abusive_count == 0:
        return "Low"
    if prob < 0.2:
        return "Low"
    elif prob < 0.5:
        return "Medium"
    else:
        return "High"

def analyze_text(text):
    text = normalize_censored(text)
    cleaned = clean_text(text)
    pred = pipeline.predict([cleaned])[0]
    prob = pipeline.predict_proba([cleaned])[0][1]
    abusive_tokens = detect_abusive_tokens(text)
    polarity = TextBlob(text).sentiment.polarity
    sentiment = "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"
    return cleaned, pred, prob, abusive_tokens, sentiment, polarity

def build_abuse_table(abusive_tokens):
    return pd.DataFrame({
        "Abusive Word": abusive_tokens,
        "Suggested Replacement": [
            suggestions.get(w.lower(), "—") for w in abusive_tokens
        ]
    })

def non_abusive_wordcloud(text, abusive_tokens):
    words = [
        w for w in clean_text(text).split()
        if w not in abusive_tokens and w not in stop_words
    ]
    if not words:
        return None
    return WordCloud(
        width=800,
        height=400,
        background_color="black",
        colormap="cool"
    ).generate(" ".join(words))

def abusive_wordcloud(abusive_tokens):
    if not abusive_tokens:
        return None
    freq = Counter([w.lower() for w in abusive_tokens])
    return WordCloud(
        width=800,
        height=400,
        background_color="black",
        colormap="autumn"
    ).generate_from_frequencies(freq)

# ---------------- Header ----------------
st.markdown("""
<h1 style="text-align:center;font-size:3rem;color:#38bdf8;">
🛡️ ToxiGuard AI
</h1>
<p style="text-align:center;color:#e5e7eb;">
Real-time Abuse Detection • Sentiment • Toxicity Analytics
</p>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("<h2>⚙️ Control Panel</h2>", unsafe_allow_html=True)
real_time = st.sidebar.toggle("⚡ Real-Time Analysis", value=False)

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar.expander("📜 Analysis History", expanded=True):
    for i, t in enumerate(reversed(st.session_state.history[-15:]), 1):
        st.write(f"{i}. {t}")

# ---------------- Input ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#38bdf8;'>✍️ Enter text</h4>", unsafe_allow_html=True)
user_input = st.text_area("", height=160, placeholder="Type or paste text here...")
st.markdown("</div>", unsafe_allow_html=True)

analyze_clicked = st.button("🔍 Analyze")

# ---------------- Analysis ----------------
def run_analysis(text):
    cleaned, pred, prob, abusive_tokens, sentiment, polarity = analyze_text(text)
    severity = toxicity_level(prob, len(abusive_tokens))

    total = len(cleaned.split())
    abusive = len(abusive_tokens)
    clean = total - abusive

    st.session_state.history.append({
        "text": text,
        "toxicity": prob,
        "severity": severity
    })

    # KPIs
    st.markdown(f"""
    <div style="display:flex;gap:20px;">
        <div class="kpi-card">📄 Words<br><h2>{total}</h2></div>
        <div class="kpi-card">⚠️ Abusive<br><h2>{abusive}</h2></div>
        <div class="kpi-card">🧪 Toxicity<br><h2>{severity}</h2></div>
    </div>
    """, unsafe_allow_html=True)

    
    # Highlighted Text
    highlighted = text
    for w in abusive_tokens:
        highlighted = re.sub(
            f"(?i){re.escape(w)}",
            f"<span class='abusive-word'>{w}</span>",
            highlighted
        )
    st.markdown(f"<div class='glass'>{highlighted}</div>", unsafe_allow_html=True)

    # Sentiment
    st.markdown(f"""
    <div class="glass">
    <b>Prediction:</b> {'⚠️ ABUSIVE' if pred else '✅ CLEAN'}<br>
    Sentiment: <b>{sentiment}</b><br>
    Polarity: <b>{polarity:.2f}</b><br>
    Confidence: <b>{prob:.2f}</b>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🧠 Why this result?")
    reasons = []

    if abusive_tokens:
        reasons.append("Detected abusive vocabulary")
    if prob > 0.4:
        reasons.append("Semantic toxicity detected by ML model")
    if polarity < -0.3:
        reasons.append("Strong negative sentiment")
    if not reasons:
        reasons.append("No toxic indicators found")

    for r in reasons:
        st.markdown(f"- {r}")

    # Toxicity Gauge
    gauge = px.bar(
        x=[prob], y=["Toxicity"], orientation="h",
        range_x=[0, 1], text=[f"{prob:.2f}"]
    )
    gauge.update_layout(height=150, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(gauge, use_container_width=True)

    # Severity Pie
    fig = px.pie(
        names=["Clean", "Abusive"],
        values=[clean, abusive]
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # Table + CSV
    if abusive_tokens:
        st.markdown("### 📊 Abusive Words & Suggestions")
        df_table = build_abuse_table(abusive_tokens)
        gb = GridOptionsBuilder.from_dataframe(df_table)
        gb.configure_default_column(sortable=True, filter=True)
        AgGrid(df_table, gridOptions=gb.build(), height=200)

        st.download_button(
            "⬇️ Download CSV",
            df_table.to_csv(index=False),
            file_name="toxiguard_report.csv",
            mime="text/csv"
        )

    # Word Clouds
    col1, col2 = st.columns(2)

    with col1:
        wc_clean = non_abusive_wordcloud(text, abusive_tokens)
        if wc_clean:
            st.markdown("### ☁️ Non-Abusive Word Cloud")
            fig, ax = plt.subplots()
            ax.imshow(wc_clean)
            ax.axis("off")
            st.pyplot(fig)

    with col2:
        wc_abuse = abusive_wordcloud(abusive_tokens)
        if wc_abuse:
            st.markdown("### 🔥 Abusive Word Cloud")
            fig, ax = plt.subplots()
            ax.imshow(wc_abuse)
            ax.axis("off")
            st.pyplot(fig)

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
Powered by <b>ToxiGuard AI</b> • NLP • Streamlit
</p>
""", unsafe_allow_html=True)
