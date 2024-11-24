from sqlalchemy import create_engine , column , INTEGER , VARCHAR , String , BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#setting connect to db
DATABASE_url = "postgresql://postgres:1234@localhost:5432/farshad2"
#craete connect to db
engine = create_engine(DATABASE_url)
SessionLocal  = sessionmaker(autocommit=False,autoflush=False,bind=engine)
#create base model
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()