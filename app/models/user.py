from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__: str = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    accounts = relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )