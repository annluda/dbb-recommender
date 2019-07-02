# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .config import *


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(db_user, db_pass, db_host, db_name)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


def upload(self):
    try:
        session.merge(self)
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


BaseModel = declarative_base()
BaseModel.upload = upload
