from fastapi import APIRouter
from src.dto.dto import UserQuery

router = APIRouter()


@router.api_route("/query", methods=["POST"])
async def query(rq: UserQuery):
    # print(query)
    pass
