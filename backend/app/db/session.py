from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
