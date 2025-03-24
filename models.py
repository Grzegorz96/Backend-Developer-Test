from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    email = Column(String(255), unique=True, index=True)  # Unique email column
    password = Column(String(255))  # Password column
    posts = relationship("Post", back_populates="owner")  # Relationship to Post model


# Define the Post model
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    text = Column(String(255), index=True)  # Text column
    owner_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User model
    owner = relationship("User", back_populates="posts")  # Relationship to User model
