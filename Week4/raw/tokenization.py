import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

text = "strawberry"

tokens = encoding.encode(text)

print("Text:", text)
print("Token IDs:", tokens)
print("Number of tokens:", len(tokens))

print("\nDecoded tokens:")

for token_id in tokens:
    print(token_id, repr(encoding.decode([token_id])))
    
    
    
    
    
    
    
    
import random

next_words = {
    "I": ["am"],
    "am": ["learning", "going"],
    "learning": ["Python", "AI"],
    "going": ["to"],
    "to": ["school", "work"],
    "Python": ["today"],
    "AI": ["today"],
    "school": ["today"],
    "work": ["today"],
    "today": ["."]
}

text = ["learning"]

for _ in range(8):
    current_word = text[-1]

    if current_word not in next_words:
        break

    next_word = random.choice(next_words[current_word])
    text.append(next_word)

print(" ".join(text))    