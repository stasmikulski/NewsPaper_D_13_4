import re

with open("wordlist.txt") as f:
    CENSORED_WORDS = f.readlines()

def validate_comment_text(text):
    words = set(re.sub("[^\w]", " ",  text).split())
    if any(censored_word in words for censored_word in CENSORED_WORDS):
        raise ValidationError(f"{censored_word} is censored!")