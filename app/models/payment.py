from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .mixins.created import CreatedMixin
from .base import Base


class Payment(Base, CreatedMixin):
    __tablename__: str = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Float, nullable=False)
    account = relationship(
        "Account",
        back_populates="payments",
        lazy="selectin"
    )