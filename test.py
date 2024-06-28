import re

def extract_word_after_at(text):
    pattern = r'@(\w+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def extract_words_after_at(text):
    pattern = r'@(\w+)'
    matches = re.findall(pattern, text)
    return matches

text = "Hey @user1 and @user2, can you help me with something?"
results = extract_words_after_at(text)
text = "@Cseven how are you"
result = extract_word_after_at(text)
print(result)
