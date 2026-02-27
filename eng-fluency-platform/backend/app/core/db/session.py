from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    # Standard settings for high performance
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_db(tenant_id: str) -> Generator[Session, None, None]:
    """
    Get a database session with Row-Level Security (RLS) initialized for a specific tenant.
    This assumes that the database has RLS policies using 'app.current_tenant'.
    """
    db = SessionLocal()
    try:
        # Set the tenant context for RLS policies
        db.execute(text(f"SET app.current_tenant = '{tenant_id}'"))
        yield db
    finally:
        db.close()
