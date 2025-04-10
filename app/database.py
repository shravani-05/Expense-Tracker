from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Make sure models.py uses this same Base

# SQLite DB file
DATABASE_FILE = "expense_tracker.db"
CONNECTION_STRING = "sqlite:///" + DATABASE_FILE

# Engine setup
engine = create_engine(CONNECTION_STRING, echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Session getter
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Create all tables
Base.metadata.create_all(bind=engine)
