"""
Script Name : resources.py
Description : Defines the CRUD API endpoints for managing developer resources.
Usage       : python3 resources.py [args]
Author      : @tonybnya
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceOut, ResourceUpdate

router = APIRouter(prefix="/resources", tags=["Resources"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", tags=["Root"])
def read_root():
    return {
        "name": "Resourcify API",
        "version": "1.0.0",
        "description": "Welcome to the Resourcify API 👋. Use this service to create, read, update, and delete curated developer resources.",
        "endpoints": {
            "List all resources": "GET /resources",
            "Get a resource": "GET /resources/{resource_id}",
            "Create a resource": "POST /resources",
            "Update a resource": "PUT /resources/{resource_id}",
            "Delete a resource": "DELETE /resources/{resource_id}",
        },
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@router.post("/", response_model=ResourceOut)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.get("/", response_model=list[ResourceOut])
def read_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()


@router.get("/{resource_id}", response_model=ResourceOut)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    res = db.query(Resource).filter(Resource.id == resource_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    return res


@router.put("/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, updated: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"detail": "Resource deleted"}
