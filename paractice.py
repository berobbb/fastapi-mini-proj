from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="sqlite:///company.db"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
from sqlalchemy import Column, Integer, String,Float,Boolean
class Employee:
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    salary=Column(Float)

class Product:
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    price=Column(Float)
    in_stock=Column(Boolean,default=True)