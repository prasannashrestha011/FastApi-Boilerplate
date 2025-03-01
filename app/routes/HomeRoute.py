from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/")
def Home():

    return JSONResponse(content={"user": "hello user"})
