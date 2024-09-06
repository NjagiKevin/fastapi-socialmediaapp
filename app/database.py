from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


# Defines the URL for connecting to the PostgreSQL database using SQLAlchemy.
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is responsible for managing the connection to the database
engine=create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is a factory for creating new session instances.
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class for all models in SQLAlchemy. All models will inherit from this.
Base=declarative_base() 

# A generator function that provides a session to interact with the database and ensures it is closed after the request is processed.
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#connecting to our db using raw sql
#try:
    #conn=psycopg2.connect(host='localhost',database='fastapi', 
                          #user='postgres', password='Tahani#21#',
                          #cursor_factory=RealDictCursor)
    
    #cursor=conn.cursor() #what we'll use to execute sql queries
    #print("Database connection was successful!!")

#except Exception as error:
    #print("Connectimg to database failed!!!")
    #print("Error", error)

