import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model_name = "gemini-2.5-flash-native-audio-latest"
print(f"Testing TTS with model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        "Read this sentence: Hello world.",
        generation_config=genai.types.GenerationConfig(
            response_mime_type="audio/wav"
        )
    )
    
    audio_present = False
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            audio_present = True
            print(f"Success! Audio data received. Size: {len(part.inline_data.data)} bytes")
            break
            
    if not audio_present:
        print("Failure: No audio data found in response.")
except Exception as e:
    print(f"TTS Test Failure: {e}")
