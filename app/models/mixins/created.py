from sqlalchemy import DateTime, func, Column


class CreatedMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)