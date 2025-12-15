import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))

APP_COLORS = {
    "background": "black",
    "font": "white",
    "highlight": "#00e5ff",
    "abusive": "#e53935",
    "non_abusive": "#43a047"
}
