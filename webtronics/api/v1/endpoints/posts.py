from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics import models, schemas, crud
from webtronics.api.deps import get_db_session, get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
async def read_posts(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    if crud.user.is_superuser(current_user):
        posts = await crud.post.get_multi(db, skip=skip, limit=limit)
    else:
        posts = await crud.post.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return posts


@router.post("/", response_model=schemas.Post)
async def create_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    post_in: schemas.PostCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    post = await crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=current_user.id)
    return post


@router.put("/{pk}/", response_model=schemas.Post)
async def update_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int,
    post_in: schemas.PostUpdate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    post = await crud.post.get(db=db, pk=pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_status.HTTP_404_NOT_FOUND_NOT_FOUND, detail="Post not found")
    if not crud.user.is_superuser(current_user) and (post.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough permissions"
        )
    post = await crud.post.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.get("/{pk}/", response_model=schemas.Post)
async def read_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    post = await crud.post.get(db=db, pk=pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.put("/{pk}/like/", response_model=schemas.Post)
async def like_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    post = await crud.post.get(db=db, pk=pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post owner can not like his own post"
        )

    await crud.post.like(db=db, post_id=pk, user_id=current_user.id)

    return post


@router.put("/{pk}/dislike/", response_model=schemas.Post)
async def dislike_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    post = await crud.post.get(db=db, pk=pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post owner can not dislike his own post"
        )

    await crud.post.dislike(db=db, post_id=pk, user_id=current_user.id)

    return post


@router.delete("/{pk}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    *,
    db: AsyncSession = Depends(get_db_session),
    pk: int,
    current_user: models.User = Depends(get_current_active_user),
):
    post = await crud.post.get(db=db, pk=pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if not crud.user.is_superuser(current_user) and (post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    await crud.post.remove(db=db, pk=pk)
