import os
import io
from openai import OpenAI
from pydub import AudioSegment
from app.core.config import settings
from app.schemas.audio import TranscriptionResult

class ASRService:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def convert_to_wav(self, audio_bytes: bytes, format: str = "webm") -> io.BytesIO:
        """
        Convert incoming audio stream chunks (often webm) to WAV/MP3 for Whisper.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        buffer = io.BytesIO()
        audio.export(buffer, format="mp3")
        buffer.name = "audio.mp3"
        buffer.seek(0)
        return buffer

    async def transcribe(self, audio_buffer: io.BytesIO) -> TranscriptionResult:
        """
        Send audio to OpenAI Whisper for transcription.
        """
        try:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_buffer,
                response_format="json"
            )
            return TranscriptionResult(
                text=transcript.text,
                language="en" # Whisper detects, but we default/force EN for pedagogical reasons
            )
        except Exception as e:
            print(f"ASR Error: {e}")
            return TranscriptionResult(text="", confidence=0.0)

asr_service = ASRService()
