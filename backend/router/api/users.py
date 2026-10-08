
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/")
def index():
    return {"message": "Router working"}

