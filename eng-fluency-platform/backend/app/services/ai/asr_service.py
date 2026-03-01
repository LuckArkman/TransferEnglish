import os
import io
import google.generativeai as genai
from app.core.config import settings
from app.schemas.audio import TranscriptionResult

class ASRService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GOOGLE_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # gemini-2.5-flash supports generateContent AND multimodal audio input
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None

    def detect_audio_mime(self, audio_bytes: bytes) -> str:
        """Detect audio mime type from raw bytes."""
        # WebM/Matroska EBML magic bytes
        if audio_bytes[:4] == b'\x1a\x45\xdf\xa3':
            return "audio/webm"
        # OGG magic bytes
        if audio_bytes[:4] == b'OggS':
            return "audio/ogg"
        # MP3 sync word or ID3 tag
        if audio_bytes[:3] == b'ID3' or audio_bytes[:2] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'):
            return "audio/mp3"
        # WAV RIFF magic bytes
        if audio_bytes[:4] == b'RIFF':
            return "audio/wav"
        # Default to webm for browser-recorded audio
        return "audio/webm"

    async def transcribe(self, audio_data: bytes) -> TranscriptionResult:
        """
        Send raw audio bytes directly to Google Gemini for transcription.
        No ffmpeg conversion needed — Gemini handles WebM/MP3/OGG natively.
        """
        if not self.model:
            print("ASR Error: Google API Key not configured")
            return TranscriptionResult(text="")

        if not audio_data or len(audio_data) < 100:
            return TranscriptionResult(text="")

        try:
            mime_type = self.detect_audio_mime(audio_data)
            print(f"ASR: Sending {len(audio_data)} bytes as {mime_type} to Gemini 2.5 Flash")

            response = self.model.generate_content([
                {
                    "mime_type": mime_type,
                    "data": audio_data
                },
                "Please transcribe this audio accurately. Reply with only the spoken text."
            ])

            text = response.text.strip() if response.text else ""
            print(f"ASR Result: '{text}'")
            return TranscriptionResult(text=text, language="en")

        except Exception as e:
            err_msg = str(e)
            if "API key not valid" in err_msg:
                print(f"CRITICAL: Gemini API Key is invalid. Check .env file.")
            elif "429" in err_msg or "quota" in err_msg.lower():
                print(f"WARNING: Gemini quota exceeded. Check your plan.")
            else:
                print(f"ASR (Gemini) Error: {e}")
            return TranscriptionResult(text="")

asr_service = ASRService()
