from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.models import Base


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_tables():
    """Create any tables that do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session and close it when finished."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
