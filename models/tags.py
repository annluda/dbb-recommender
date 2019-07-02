# _*_ coding:utf-8 _*_
from models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime


class Tags(BaseModel):
    __tablename__ = 'tags'
    tag = Column(String(255), primary_key=True)

