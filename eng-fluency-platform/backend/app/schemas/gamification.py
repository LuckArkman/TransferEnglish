from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AchievementBase(BaseModel):
    name: str
    description: str
    icon: Optional[str] = None

class UserAchievement(BaseModel):
    achievement_id: str
    awarded_at: datetime

    class Config:
        from_attributes = True

class UserRewards(BaseModel):
    achievements: List[AchievementBase]
    streaks: int
    total_points: int
