import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model_name = "gemini-2.5-flash-tts"
print(f"Testing blind TTS with model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello, this is LuckArkman Engine v2.5 test. Speak this text.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"TTS Test Failure: {e}")
