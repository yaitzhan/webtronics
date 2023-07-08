from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from webtronics.db.base_class import Base
from webtronics.models.abstract_models import CreatedAtUpdatedAtAbstractModel


class Post(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", backref="posts")
    like = relationship("Like", back_populates="post", uselist=False)


class UsersLikes(Base):
    __tablename__ = "users_likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    like_id = Column(Integer, ForeignKey("like.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    like = relationship("Like", back_populates="users_likes")
    user = relationship("User", back_populates="users_likes")


class Like(CreatedAtUpdatedAtAbstractModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"))

    post = relationship("Post", back_populates="like")
    users_likes = relationship("UsersLikes", back_populates="like")
