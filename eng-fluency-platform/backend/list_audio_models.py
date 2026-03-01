import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

print("\nSearching for models with audio output support...")
try:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"Name: {m.name}")
            # Try to see if we can find more info about mime types
            # Actually, the only way is to try it.
except Exception as e:
    print(f"Error: {e}")
