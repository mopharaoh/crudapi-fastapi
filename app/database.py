from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")
engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn=psycopg2.connect(host="localhost",database='fastapi',user='postgres',password='password',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("db was succesfull")
#         break
#     except Exception as error:
#         print('connection is failed')
#         print('error : ',error)
#         time.sleep(2)

