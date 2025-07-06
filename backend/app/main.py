"""
Script Name : main.py
Description : Bootstraps the FastAPI app, connects routes, and initializes the database.
Usage       : python3 main.py [args]
Author      : @tonybnya
"""

from fastapi import FastAPI

from app.api.routes import resources
from app.core.database import Base, engine

app = FastAPI(title="Resourcify API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(resources.router)


@app.get("/", tags=["Root"])
def root_info():
    return {
        "message": "Welcome to Resourcify API 🎉",
        "versioned_entry": "/api/v1/resources",
        "interactive docs": "/docs",
        "alternative docs": "/redoc",
    }
