from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.Models.UserModels import RegisterResponse, AuthResponse


from app.lib.jwt import JwtService
from app.configs.db import get_session

from app.services.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(db: AsyncSession = Depends(get_session)):
    return AuthService(db)


@router.post("/register")
async def Register_User(
    user_details: RegisterResponse, auth_service: AuthService = Depends(get_service)
):
    print("Received details->", user_details)
    register_response = await auth_service.register_user(user_details)
    print(register_response)
    return JSONResponse(
        content={"message": register_response.message},
        status_code=register_response.status_code,
    )


@router.post("/login")
async def Login_user(
    user_details: AuthResponse, auth_service: AuthService = Depends(get_service)
):
    print(user_details)
    auth_response = await auth_service.login_user(user_details)

    if auth_response.success is False:
        return JSONResponse(
            content={"message": auth_response.message},
            status_code=auth_response.status_code,
        )
    access_token = auth_response.data["access_token"]
    refresh_token = auth_response.data["refresh_token"]
    return JSONResponse(
        content={"message": auth_response.message},
        status_code=auth_response.status_code,
        headers={
            "Authorization": f"Bearer {access_token}",
            "RefreshToken": f"Bearer {refresh_token}",
        },
    )


@router.get("/refresh/access_token")
async def Refresh_Access_Token(request: Request):
    refresh_token = request.headers.get("refreshtoken")
    refresh_token = refresh_token.split("Bearer ")[1]
    if refresh_token is None:
        return JSONResponse(
            content={"error": "Refresh token not found"}, status_code=400
        )
    token_response = JwtService.renew_access_token(refresh_token=refresh_token)

    if token_response.access_token is None and token_response.error:
        return JSONResponse(content={"error": token_response.error}, status_code=400)

    return JSONResponse(
        content={"message": "access token refreshed"},
        status_code=200,
        headers={"Authorization": f"Bearer {token_response.access_token}"},
    )
