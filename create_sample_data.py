import pandas as pd

data = {
    "text": ["I hate you", "You are amazing", "This is stupid", "Have a great day", "Idiot!", "Thank you for helping"],
    "label": ["abusive", "non-abusive", "abusive", "non-abusive", "abusive", "non-abusive"]
}

df = pd.DataFrame(data)

# Create a folder named 'data' if it doesn't exist
import os
if not os.path.exists("data"):
    os.makedirs("data")

df.to_csv("data/sample_data.csv", index=False)
print("sample_data.csv created in the data/ folder!")
