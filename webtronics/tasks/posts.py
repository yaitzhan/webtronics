import json

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics import crud


async def cache_likes_dislikes(
        *,
        db: AsyncSession,
        redis: Redis,
        post_id: int
):
    likes = await crud.post.get_likes_count(db=db, post_id=post_id)
    dislikes = await crud.post.get_dislikes_count(db=db, post_id=post_id)

    data = json.dumps({"likes": likes, "dislikes": dislikes})

    async with redis.client() as conn:
        await conn.set(str(post_id), data)
