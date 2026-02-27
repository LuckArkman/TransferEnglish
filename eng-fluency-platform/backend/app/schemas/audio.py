from pydantic import BaseModel
from typing import Optional, List

class TranscriptionResult(BaseModel):
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = "en"
    duration: Optional[float] = None

class AudioFileMetadata(BaseModel):
    format: str
    channels: int
    sample_rate: int
