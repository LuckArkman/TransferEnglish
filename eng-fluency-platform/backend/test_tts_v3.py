import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model_name = "gemini-2.5-flash-tts"
print(f"Testing TTS with model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    # Just text, no special config
    response = model.generate_content("Hello world")
    
    print(f"Response Parts: {len(response.candidates[0].content.parts)}")
    for i, part in enumerate(response.candidates[0].content.parts):
        print(f"Part {i} Type: {type(part)}")
        if part.inline_data:
            print(f"Part {i} Inline Data Mime: {part.inline_data.mime_type}")
            print(f"Part {i} Data Size: {len(part.inline_data.data)}")
        if part.text:
            print(f"Part {i} Text: {part.text}")
            
except Exception as e:
    print(f"TTS Test Failure: {e}")
