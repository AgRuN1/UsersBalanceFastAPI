from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Account(Base):
    __tablename__: str = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship(
        "User",
        back_populates="accounts",
        lazy="selectin"
    )
    payments = relationship(
        "Payment",
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin"
    )