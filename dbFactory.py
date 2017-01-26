from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
class TodoItem(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    item = Column(String)

def initDbSession():
	db = create_engine("sqlite:///todolist.sqlite")
	session = sessionmaker()
	session.configure(bind=db)
	Base.metadata.create_all(db)
	return session