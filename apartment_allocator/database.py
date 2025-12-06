from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///apartment_allocator.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database and create all tables"""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Get a database session"""
    return SessionLocal()