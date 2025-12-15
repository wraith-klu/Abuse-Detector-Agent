import re
from .abuse_words import abusive_words

def highlight_abusive(text: str):
    abusive_tokens = [w for w in re.findall(r'\b\w+\b', text.lower()) if w in abusive_words]
    highlighted_text = text
    for word in abusive_tokens:
        highlighted_text = re.sub(
            f"(?i){re.escape(word)}",
            f"<span style='background-color:#ff5252;color:white;padding:2px 4px;border-radius:4px;'>{word}</span>",
            highlighted_text
        )
    return highlighted_text, abusive_tokens
