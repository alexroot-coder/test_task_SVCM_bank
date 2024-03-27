from database import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, JSON, Integer, ARRAY, ForeignKey, UUID


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    city = Column(String)
    street = Column(String)
    building = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="address")
