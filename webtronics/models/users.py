from sqlalchemy import Integer, Boolean, Column, String

from webtronics.models.abstract_models import CreatedAtUpdatedAtAbstractModel


class User(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128))
    email = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username})>'
