from fastapi import APIRouter


from webtronics.api.v1.endpoints import auth
from webtronics.api.v1.endpoints import users
from webtronics.api.v1.endpoints import posts

router = APIRouter()
router.include_router(auth.router,  prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
