from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.gamification import Achievement, UserAchievement
from app.schemas.gamification import AchievementBase, UserRewards
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserRewards)
def get_user_achievements(
    db: Session = Depends(deps.get_db_with_tenant),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve user achievements, points, and streaks.
    """
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    achievements = [db.query(Achievement).get(ua.achievement_id) for ua in user_achievements]
    
    return UserRewards(
        achievements=[AchievementBase(name=a.name, description=a.description, icon=a.icon) for a in achievements],
        streaks=5, # Placeholder streak
        total_points=1200 # Placeholder points
    )
