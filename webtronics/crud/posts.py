from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics.crud.base import CRUDBase
from webtronics.models.posts import Post, Like, Dislike, UsersLikes, UsersDislikes
from webtronics.schemas.posts import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: PostCreate, owner_id: int
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)

        # create like object
        await db.flush()
        like_obj = Like(post_id=db_obj.id)
        db.add(like_obj)

        # create dislike object
        await db.flush()
        like_obj = Dislike(post_id=db_obj.id)
        db.add(like_obj)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        query = select(self.model).filter(self.model.owner_id == owner_id).offset(skip).limit(limit)
        rows = await db.execute(query)
        return rows.scalars().all()

    async def like(
        self, db: AsyncSession, *, post_id: int, user_id: int,
    ):
        select_query = select(UsersLikes).filter_by(user_id=user_id)
        res = await db.execute(select_query)
        row = res.first()
        if row is None:
            like_select_query = select(Like).filter_by(post_id=post_id)
            res = await db.execute(like_select_query)
            like_obj = res.scalar_one_or_none()
            if like_obj:
                data_in_list = [
                    {
                        "like_id": like_obj.id,
                        "user_id": user_id
                    }
                ]
                await db.execute(UsersLikes.__table__.insert(), data_in_list)
            delete_query = delete(UsersDislikes).filter_by(user_id=user_id)
            await db.execute(delete_query)
            await db.commit()
        else:
            query = delete(UsersLikes).filter_by(user_id=user_id)
            await db.execute(query)
            await db.commit()

    async def dislike(
        self, db: AsyncSession, *, post_id: int, user_id: int,
    ):
        select_query = select(UsersDislikes).filter_by(user_id=user_id)
        res = await db.execute(select_query)
        row = res.first()
        if row is None:
            dislike_select_query = select(Dislike).filter_by(post_id=post_id)
            res = await db.execute(dislike_select_query)
            dislike_obj = res.scalar_one_or_none()
            if dislike_obj:
                data_in_list = [
                    {
                        "dislike_id": dislike_obj.id,
                        "user_id": user_id
                    }
                ]
                await db.execute(UsersDislikes.__table__.insert(), data_in_list)
            delete_query = delete(UsersLikes).filter_by(user_id=user_id)
            await db.execute(delete_query)
            await db.commit()
        else:
            query = delete(UsersDislikes).filter_by(user_id=user_id)
            await db.execute(query)
            await db.commit()


post = CRUDPost(Post)
