"""
Script Name : database.py
Description : Sets up the SQLite connection, SQLAlchemy engine, and session maker.
Usage       : python3 database.py [args]
Author      : @tonybnya
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./resourcify.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
