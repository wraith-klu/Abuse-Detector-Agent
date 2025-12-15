# abuse_words.py
import re

# Abusive words set
abusive_words = { "idiot","stupid","dumb","hate","kill","loser","pathetic","ugly","shit",
"fool","trash","nonsense","moron","jerk","worthless","suck","sh*t","bastard","crap","damn","hell",
"foolish","f**k","go to hell","bitch","asshole","a**hole","fuck","fucking","fucked","fucker","fucks",
"fuk","fuking","fuked","fuker","motherf**ker","ass","piss","wtf","chodu","madarchod","randi","behenchod",
"lund","gandu","bhosdike","bhadwe","sala","chutiya","pagal","bewakoof","harami","kaminey","kutte","lodu",
"bullshit","bullsh*t","andhbhakt","tatti","bakwas","bkl","bc" }
abusive_words = set(word.lower() for word in abusive_words)

# Suggestions dictionary
suggestions = {
    "idiot":"Try saying 'uninformed' or 'mistaken'.",
    "stupid":"Use 'unwise' or 'not a great idea'.",
    "hate":"Replace with 'dislike' or 'prefer not to'.",
    "kill":"Say 'stop' or 'end' instead.",
    "fool":"Try 'misguided person' or 'uninformed'.",
    "shit":"Use 'mess' or 'trouble'.",
    "ugly":"You can say 'not appealing' or 'different looking'.",
    "bitch":"Consider 'rude person' or just skip it.",
    "fuck":"Avoid it; express calmly or use 'mess up'.",
    "gandu":"Avoid slang; use respectful disagreement.",
    "chutiya":"Avoid personal insults; express disagreement politely.",
    "harami":"Avoid such words; you can say 'unfair' or 'wrongdoing'.",
    "pagal":"Say 'confused' or 'silly' instead.",
    "bewakoof":"Say 'mistaken' or 'wrong idea'.",
    "loser":"Say 'unlucky' or 'didn’t win this time'.",
    "damn":"You can skip it or say 'oh no'."
}

# ---------------- Function to detect abusive tokens ----------------
def detect_abusive_tokens(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [t for t in tokens if t in abusive_words]
