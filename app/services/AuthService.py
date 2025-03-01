from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.Models.UserModels import RegisterResponse, AuthResponse, UserModel
from app.Models.ResponseModel import ResponseModel
from app.lib.hashing import hash_password, verify_password
from app.lib.jwt import JwtService
from typing import Optional


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_user(
        self, username: Optional[str] = None, email: Optional[str] = None
    ) -> Optional[UserModel]:
        statement = select(UserModel).where(
            (UserModel.username == username) | (UserModel.email == email)
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def register_user(self, user_details: RegisterResponse):
        try:
            # validation
            _exists_user = await self.fetch_user(user_details.username)
            if _exists_user:
                message = (
                    "Email already taken"
                    if _exists_user.email == user_details.email
                    else "Username already taken"
                )
                return ResponseModel(message=message, status_code=400)

            # hash pwd
            user_details.password = hash_password(user_details.password)
            user_entity = UserModel(
                username=user_details.username,
                password=user_details.password,
                email=user_details.email,
                full_name=user_details.full_name,
            )
            self.db.add(user_entity)
            await self.db.commit()
            self.db.refresh(user_entity)
            return ResponseModel(
                message="Registration sucessfull", success=True, data={user_entity.id}
            )
        except Exception as e:
            print("Unknow error->", e)
            return ResponseModel(message="Unknow error", status_code=500)

    async def login_user(self, auth_details: AuthResponse) -> ResponseModel:
        try:
            email_or_username = (
                auth_details.email if auth_details.email else auth_details.username
            )
            auth_user = await self.fetch_user(email_or_username)
            if auth_user is None:
                return ResponseModel(message="User not found", status_code=404)

            verified_user = verify_password(
                plain_pwd=auth_details.password, hashed_pwd=auth_user.password
            )
            if verified_user is False:
                return ResponseModel(
                    message="Incorrect password,try again", status_code=403
                )

            auth_tokens = JwtService.create_token(username=auth_user.username)

            return ResponseModel(
                message="Authentication successful", success=True, data=auth_tokens
            )
        except Exception as e:
            print("Error", e)
            return ResponseModel(message="Unknown error has occurred", status_code=500)
