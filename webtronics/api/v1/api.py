from fastapi import APIRouter


from webtronics.api.v1.endpoints import auth

router = APIRouter()
router.include_router(auth.router, tags=["auth"])
