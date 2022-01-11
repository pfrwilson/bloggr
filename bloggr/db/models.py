from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import MetaData

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    
    posts = relationship('Post', back_populates="owner")
    
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    datecreated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    owner = relationship('User', back_populates='posts')

metadata: MetaData = Base.metadata


