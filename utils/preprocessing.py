import re

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
