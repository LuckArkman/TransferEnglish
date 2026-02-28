from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, TenantMixin
import uuid

class Achievement(Base, TimestampMixin, TenantMixin):
    __tablename__ = "achievements"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str] = mapped_column(String(50), nullable=True) # Icon ID/Emoji
    criteria_type: Mapped[str] = mapped_column(String(50)) # e.g., 'sessions_count', 'ifp_score', 'streak'
    criteria_value: Mapped[int] = mapped_column(Integer)

class UserAchievement(Base, TimestampMixin, TenantMixin):
    __tablename__ = "user_achievements"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    achievement_id: Mapped[str] = mapped_column(String, ForeignKey("achievements.id"))
    awarded_at: Mapped[str] = mapped_column(String, nullable=True)
