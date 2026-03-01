import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model_name = "gemini-3-flash-preview"
print(f"Testing TTS with model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        "Hello from Gemini 3 Flash.",
        generation_config=genai.types.GenerationConfig(
            response_mime_type="audio/wav"
        )
    )
    
    if any(part.inline_data for part in response.candidates[0].content.parts):
        print("SUCCESS! Gemini 3 Flash supports audio output!")
    else:
        print("No audio output in response.")
except Exception as e:
    print(f"Test failure: {e}")
