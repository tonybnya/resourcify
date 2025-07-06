"""
Script Name : resource.py
Description : Defines the Resource model/table with fields like name, type, tags, etc.
Usage       : python3 resource.py [args]
Author      : @tonybnya
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.types import JSON

from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String)
    category = Column(String)
    platform = Column(String)
    cost = Column(String)
    description = Column(Text)
    tags = Column(JSON)
