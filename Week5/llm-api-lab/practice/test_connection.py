import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

print("API key loaded:", bool(api_key))
print("Groq client created successfully!")
