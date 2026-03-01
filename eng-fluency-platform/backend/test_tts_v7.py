import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model_name = "models/gemini-2.5-flash-tts"
print(f"Testing blind TTS for model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello! This is an audio test.")
    
    for i, part in enumerate(response.candidates[0].content.parts):
        print(f"Part {i} Content: {part}")
except Exception as e:
    print(f"Failure: {e}")
