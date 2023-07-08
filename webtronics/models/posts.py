from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from webtronics.models.abstract_models import CreatedAtUpdatedAtAbstractModel


class Post(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", backref="posts")
