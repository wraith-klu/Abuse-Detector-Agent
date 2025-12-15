# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import joblib
from utils.preprocessing import clean_text, normalize_censored

# ---------------- Load dataset ----------------
data = pd.read_csv("data/sample_data.csv")  # updated path

# Convert labels to 0 (non-abusive) and 1 (abusive)
data['label'] = data['label'].map({"non-abusive": 0, "abusive": 1})

# Clean the text
data['text'] = data['text'].apply(lambda x: clean_text(normalize_censored(str(x))))

X = data['text']
y = data['label']

# ---------------- Split data ----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------- Create pipeline ----------------
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', LogisticRegression(max_iter=1000))
])

# ---------------- Train model ----------------
pipeline.fit(X_train, y_train)

# ---------------- Evaluate ----------------
accuracy = pipeline.score(X_test, y_test)
print(f"Model accuracy: {accuracy*100:.2f}%")

# ---------------- Save model ----------------
joblib.dump(pipeline, "abuse_model.joblib")
print("Model saved as 'abuse_model.joblib'")
