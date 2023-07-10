from sqlalchemy import Integer, Boolean, Column, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from webtronics.models.abstract_models import CreatedAtUpdatedAtAbstractModel


class User(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128))
    email = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    users_likes = relationship("UsersLikes", back_populates="user")
    users_dislikes = relationship("UsersDislikes", back_populates="user")
    additional = relationship("UserAdditional", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class UserAdditional(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # we may also store 3d party data as json field
    # some clearbit fields
    full_name = Column(String(100), nullable=True)
    time_zone = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    # some email-hunter fields
    email_status = Column(String(100), nullable=True)
    email_score = Column(SmallInteger, nullable=True)
    email_disposable = Column(Boolean, nullable=True)
    email_gibberish = Column(Boolean, nullable=True)

    user = relationship("User", back_populates="additional")

    def __repr__(self):
        return f"<UserAdditional(id={self.id}"
