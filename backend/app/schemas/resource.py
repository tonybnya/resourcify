"""
Script Name : resource.py
Description : Defines data schemas for creating, updating, and returning Resource objects.
Usage       : python3 resource.py [args]
Author      : @tonybnya
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ResourceBase(BaseModel):
    name: str
    category: Optional[str] = None
    platform: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    pass


class ResourceOut(ResourceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
