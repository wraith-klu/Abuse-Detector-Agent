**Abuse-Detector-Agent**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25-orange?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

-> **🛡️ ToxiGuard AI – Abuse Detection System (AI Project)**
- *🧠 Tech Stack: Python | Streamlit | NLP | Machine Learning | Plotly*

- ⚡ Real-time detection of abusive/toxic language with sentiment classification
- 🎯 Confidence scoring with abusive keyword highlighting & severity analysis
- 📊 Interactive analytics dashboard for NLP insights
- 🎨 Clean, scalable UI with custom CSS (production-ready)
- **🔗 Repo:** [GitHub](https://github.com/wraith-klu/Abuse-Detector-Agent.git) | **🌐 Live:** [Link](https://toxiguardagent.streamlit.app/)

- **Real-time AI-based abuse detector and text analysis tool** with sentiment insights, toxicity reporting, and word-level suggestions.

---

## 🚀 Features

- Detects abusive language in real-time text input.
- Highlights abusive words and provides polite replacement suggestions.
- Sentiment analysis (Positive, Neutral, Negative) with polarity scores.
- Toxicity gauge and severity distribution visualizations.
- Word frequency analysis and word cloud (non-abusive context).
- Interactive data table with sortable/filterable abusive words.
- Downloadable CSV report of abusive words and suggestions.
- History tracking of previous analyses.

---

## 🛠️ Tech Stack

- **Backend:** Python, Streamlit
- **Machine Learning:** Scikit-learn, Joblib
- **NLP:** NLTK, TextBlob, Langdetect
- **Visualization:** Plotly, WordCloud, Matplotlib
- **Frontend:** Streamlit UI components, AgGrid

---

## 📂 Repository Structure

```

Abuse-Detector-Agent/
├── assets/                 # Images, background files, UI assets
├── data/                   # Sample or training datasets
├── utils/                  # Helper functions for preprocessing, cleaning, etc.
├── abuse_model.joblib      # Trained ML model
├── create_sample_data.py   # Script to generate sample data
├── main.py                 # Main Streamlit app
├── requirements.txt        # Python dependencies
├── train_model.py          # Script to train the abuse detection model

````

---

## 💻 Installation

1. **Clone the repository**

```bash
git clone https://github.com/wraith-klu/Abuse-Detector-Agent.git
cd Abuse-Detector-Agent
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ Running the App

```bash
streamlit run main.py
```

* Open your browser at the URL shown in the terminal (usually `http://localhost:8501`)
* Enter text in the input box and click **Analyze Sentence** to see the predictions and insights.

---

## 📊 Usage Examples

* Detect abusive content in chat messages, comments, or social media text.
* Get sentiment insights and suggested replacements for harsh words.
* Visualize abusive word severity and frequency in interactive plots.

---

## ⚙️ Notes

* Make sure `abuse_model.joblib` is present in the root directory.
* Background images and assets are in the `assets/` folder.
* Stopwords are downloaded via NLTK automatically on first run.

---

## 📄 License

MIT License © 2025 Wraith-KLU

---

## 📞 Contact

Developed by **Saurabh Yadav**
GitHub: [https://github.com/wraith-klu](https://github.com/wraith-klu)

