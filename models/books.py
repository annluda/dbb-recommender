# _*_ coding:utf-8 _*_
from models import BaseModel
from sqlalchemy import Column, Integer, String


class Books(BaseModel):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

