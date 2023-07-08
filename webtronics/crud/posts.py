from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics.crud.base import CRUDBase
from webtronics.models.posts import Post
from webtronics.schemas.posts import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: PostCreate, owner_id: int
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        query = select(self.model).filter(self.model.owner_id == owner_id).offset(skip).limit(limit)
        rows = await db.execute(query)
        return rows.scalars().all()


post = CRUDPost(Post)
