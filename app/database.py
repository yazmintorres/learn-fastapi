from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password@localhost:5433/fastapi'

# engine responsible for establish connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the base class for declarative mapping
Base = declarative_base()

# Dependency, get a session to the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For reference, if choosing to run raw sql instead of SQLAlechmy
# while True:
#     try: 
#         conn = psycopg2.connect(host="localhost", database = "fastapi", user="postgres" , password="password", port="5433")
#         cursor = conn.cursor(cursor_factory=RealDictCursor)
#         print("Database connection was succesful!")
#         break
#     except Exception as error: 
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2) #seconds