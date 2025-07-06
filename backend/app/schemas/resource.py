"""
Script Name : resource.py
Description : Defines data schemas for creating, updating, and returning Resource objects.
Usage       : python3 resource.py [args]
Author      : @tonybnya
"""

from typing import Optional

from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str
    type: Optional[str] = None
    platform: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None  # store as "tag1,tag2"


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    pass


class ResourceOut(ResourceBase):
    id: int

    class Config:
        orm_mode = True
