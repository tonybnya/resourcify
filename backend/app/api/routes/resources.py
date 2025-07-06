"""
Script Name : resources.py
Description : Defines the versioned CRUD API endpoints for managing developer resources.
Prefix      : /api/v1/resources
Author      : @tonybnya
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceOut, ResourceUpdate

router = APIRouter(prefix="/api/v1/resources", tags=["Resources"])


@router.get("/", tags=["Root"])
def api_info():
    return {
        "name": "Resourcify API",
        "version": "1.0.0",
        "description": "Welcome to the Resourcify API 👋. Use this service to manage curated developer resources.",
        "routes": {
            "List all resources": "GET /api/v1/resources",
            "Get a resource": "GET /api/v1/resources/{resource_id}",
            "Create a resource": "POST /api/v1/resources",
            "Update a resource": "PUT /api/v1/resources/{resource_id}",
            "Delete a resource": "DELETE /api/v1/resources/{resource_id}",
        }
    }


@router.post("/", response_model=ResourceOut)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.get("/all", response_model=list[ResourceOut])
def read_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()


@router.get("/{resource_id}", response_model=ResourceOut)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


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
    return {"detail": f"Resource with ID {resource_id} deleted successfully."}
