import os
import io
import wave
import struct
import google.generativeai as genai
from typing import Optional
from app.core.config import settings

class TTSService:
    def __init__(self, api_key: str = None):
        self.google_api_key = api_key or settings.GOOGLE_API_KEY
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            # gemini-2.5-flash suports generateContent (text output)
            # We use it to get natural-sounding phonetic text, then synthesize with gTTS or basic audio
            self.model_name = "gemini-2.5-flash"
        else:
            self.model_name = None

    def _text_to_basic_wav(self, text: str) -> bytes:
        """
        Fallback: generate a silent WAV placeholder when TTS is unavailable.  
        The frontend will still show the AI text response even without audio.
        """
        # Return empty bytes - frontend handles text-only responses gracefully
        return b""

    async def generate_speech(self, text: str, voice_id: Optional[str] = None, settings: Optional[dict] = None) -> bytes:
        """
        Attempt to generate speech. With Gemini 2.5 Flash, audio output via
        response_mime_type is not yet supported in the standard generateContent API.
        We return empty bytes for now — the frontend shows the text response.
        The TTS capability will be enabled when the google.genai SDK (v1.0+) 
        is available and supports the SpeechConfig API.
        """
        if not self.google_api_key:
            print("Warning: GOOGLE_API_KEY missing. Skipping speech generation.")
            return b""

        # NOTE: Gemini 2.5 Flash does NOT support audio/wav response_mime_type
        # via the legacy google.generativeai package. The newer google.genai package
        # with SpeechConfig is required. For now, return empty bytes.
        # The AI text response is still sent via the 'ai_response' websocket message.
        return b""

tts_service = TTSService()
