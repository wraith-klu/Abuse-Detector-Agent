# main.py
import streamlit as st
import joblib
import re
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
from utils.abuse_words import abusive_words, suggestions, detect_abusive_tokens

# ---------------- NLTK Stopwords ----------------
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ---------------- Load Trained Model ----------------
model_path = "abuse_model.joblib"
try:
    pipeline = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ---------------- Text Preprocessing ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#\w+", " ", text)
    text = re.sub(r"[^a-z0-9\s\*]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_censored(text):
    replacements = {
        r"f\*+k": "fuck",
        r"a\*+hole": "asshole",
        r"motherf\*+ker": "motherf**ker"
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, polarity

def analyze_text(text):
    text = normalize_censored(text)
    cleaned = clean_text(text)
    prediction = pipeline.predict([cleaned])[0]
    prob = pipeline.predict_proba([cleaned])[0][1]
    abusive_tokens = detect_abusive_tokens(text)
    sentiment, polarity = get_sentiment(text)
    return cleaned, prediction, prob, abusive_tokens, sentiment, polarity

# ---------------- Streamlit Layout ----------------
st.set_page_config(page_title="Abuse Detector", page_icon="😡", layout="wide")
st.markdown("<h1 style='text-align:center; color:#00e5ff;'>🧠 Abuse Detector & Text Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#cfd8dc;'>Type your sentence and get abuse detection, sentiment & insights!</p>", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Settings")
real_time = st.sidebar.checkbox("Enable Real-Time Analysis", value=False)

# Search History
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar.expander("📜 Search History", expanded=True):
    for i, text in enumerate(reversed(st.session_state.history[-20:]), 1):
        st.write(f"{i}. {text}")

# User input
user_input = st.text_area("Enter your text:", height=180, placeholder="Type your text here...")

# ---------------- Real-Time or Button Analysis ----------------
def run_analysis(text):
    cleaned, prediction, prob, abusive_tokens, sentiment, polarity = analyze_text(text)
    total_words = len(cleaned.split())
    abusive_count = len(abusive_tokens)
    non_abusive_count = total_words - abusive_count

    # KPI cards
    st.markdown(f"""
    <div style='display:flex; justify-content:space-around; margin-bottom:20px;'>
        <div style='background:#00e5ff; padding:20px; border-radius:12px; text-align:center;'>Total Words<br>{total_words}</div>
        <div style='background:#ff5252; padding:20px; border-radius:12px; text-align:center;'>Abusive Words<br>{abusive_count}</div>
        <div style='background:#43a047; padding:20px; border-radius:12px; text-align:center;'>Non-Abusive Words<br>{non_abusive_count}</div>
    </div>
    """, unsafe_allow_html=True)

    # Highlight abusive words
    highlighted_text = user_input
    for word in abusive_tokens:
        highlighted_text = re.sub(
            f"(?i){re.escape(word)}",
            f"<span style='color:#ff5252; font-weight:bold; background:rgba(255,255,255,0.1); padding:2px 4px; border-radius:4px;'>{word}</span>",
            highlighted_text
        )
    st.markdown(f"<div style='background: rgba(255,255,255,0.08); padding:15px; border-radius:12px; margin-top:10px;'><b>Sentence:</b><br>{highlighted_text}</div>", unsafe_allow_html=True)

    # Sentiment
    st.markdown(f"**Sentiment:** {sentiment} (Polarity: {polarity:.2f})")
    st.markdown(f"**Prediction:** {'⚠️ Abusive' if prediction==1 else '✅ Clean'} (Probability: {prob:.2f})")

    # Pie chart
    df_compare = pd.DataFrame({"Type":["Abusive","Non-Abusive"],"Count":[abusive_count, non_abusive_count]})
    fig_compare = px.pie(df_compare, names='Type', values='Count',
                         color='Type', color_discrete_map={'Abusive':'#e53935','Non-Abusive':'#43a047'},
                         title="Abusive vs Non-Abusive Words")
    fig_compare.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig_compare, use_container_width=True)

    # Word Cloud
    non_abusive_words = [w for w in re.findall(r'\b\w+\b', cleaned) if w not in stop_words and w not in abusive_words]
    if non_abusive_words:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        wc = WordCloud(width=800, height=400, background_color="black", colormap="cool").generate(" ".join(non_abusive_words))
        st.markdown("<h4 style='color:#00e5ff;'>☁️ Word Cloud (Non-Abusive)</h4>", unsafe_allow_html=True)
        fig_wc, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_wc)

    # Interactive Table
    data = []
    for w in abusive_tokens:
        suggestion = suggestions.get(w, "Use polite language.")
        severity = "High" if w in ['fuck','asshole','motherf**ker','gandu'] else "Moderate"
        data.append({"Abusive Word": w, "Suggestion": suggestion, "Severity": severity})
    if data:
        df_table = pd.DataFrame(data)
        gb = GridOptionsBuilder.from_dataframe(df_table)
        gb.configure_default_column(editable=False, resizable=True, sortable=True, filter=True)
        gb.configure_grid_options(domLayout='normal', rowHeight=35)
        grid_options = gb.build()
        AgGrid(df_table, gridOptions=grid_options, height=200, theme='streamlit', allow_unsafe_jscode=True)

        # Download CSV
        csv = df_table.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Report CSV", data=csv, file_name='abuse_report.csv', mime='text/csv')

# ---------------- Run Analysis ----------------
if user_input.strip():
    # Add to history
    if user_input not in st.session_state.history:
        st.session_state.history.append(user_input)

    if real_time:
        run_analysis(user_input)
    elif st.button("Analyze Sentence"):
        run_analysis(user_input)
