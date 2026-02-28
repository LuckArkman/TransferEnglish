from pydantic import BaseModel
from typing import List, Optional

class PressureChallenge(BaseModel):
    id: str
    target_text: str
    time_limit_seconds: int
    difficulty_multiplier: float
    description: str

class PressureSessionConfig(BaseModel):
    is_active: bool = False
    current_challenge: Optional[PressureChallenge] = None
    start_time: Optional[float] = None
    total_challenges_count: int = 5
