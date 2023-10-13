from ..db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    user_name = Column(String)
    password = Column(String)

    tasks = relationship("Tasks", back_populates="id")


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(Integer, primary_key=True)
    description = Column(Integer, primary_key=True)
    completion_status = Column(Boolean, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id"))
