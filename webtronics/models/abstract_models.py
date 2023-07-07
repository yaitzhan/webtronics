from datetime import datetime

from sqlalchemy import DateTime, Column

from webtronics.db.base_class import Base


class CreatedAtUpdatedAtAbstractModel(Base):
    __abstract__ = True

    # TODO: timezone
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
