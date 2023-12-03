from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, text,ForeignKey
from .database import Base  # Make sure to import Base from your database module
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="Users"

    id=Column(Integer,primary_key=True,nullable=False)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,nullable=False,server_default=text('now()'))

class Post(Base):
    __tablename__ ="Posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP,nullable=False,server_default=text('now()'))
    owner_name=Column(String,ForeignKey("Users.username",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")


class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    is_completed = Column(Boolean, nullable=False, server_default="false")  # Change server_default to "false"
    owner_name=Column(String,ForeignKey("Users.username",ondelete="CASCADE"),nullable=False)


class Vote(Base):
    __tablename__="Votes"

    user_name=Column(String,ForeignKey("Users.username",ondelete="CASCADE"),primary_key=True,)
    post_id=Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)