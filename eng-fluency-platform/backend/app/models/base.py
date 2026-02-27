from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
import uuid

class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class TenantMixin:
    @declared_attr
    def tenant_id(cls):
        return mapped_column(String, index=True, nullable=False)
