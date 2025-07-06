"""
Script Name : resource.py
Description : Defines data schemas for creating, updating, and returning Resource objects.
Usage       : python3 resource.py [args]
Author      : @tonybnya
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ResourceBase(BaseModel):
    name: str
    category: Optional[str] = None  # formerly 'type'
    platform: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    pass


class ResourceOut(ResourceBase):
    _id: int = Field(..., alias="resource_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # enables using '_id' in responses
