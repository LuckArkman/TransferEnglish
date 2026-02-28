from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.gamification import Achievement, UserAchievement
from app.models.analytics import FluencySession
from typing import List

class GamificationService:
    @staticmethod
    def check_achievements(db: Session, user_id: str):
        """
        Check and award achievements based on user activity.
        """
        # Get count of sessions as an example criteria
        session_count = db.query(FluencySession).filter(FluencySession.user_id == user_id).count()
        
        all_achievements = db.execute(select(Achievement)).scalars().all()
        for ach in all_achievements:
            # Check if user already has it
            existing = db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == ach.id
            ).first()
            
            if not existing:
                if ach.criteria_type == 'sessions_count' and session_count >= ach.criteria_value:
                    GamificationService._award_achievement(db, user_id, ach.id)

    @staticmethod
    def _award_achievement(db: Session, user_id: str, achievement_id: str):
        ua = UserAchievement(user_id=user_id, achievement_id=achievement_id)
        db.add(ua)
        db.commit()

gamification_service = GamificationService()
