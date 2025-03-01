import uuid
from pydantic import BaseModel, model_validator, field_validator, EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional


class UserModel(SQLModel, table=True):
    __tablename__ = "user_model"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: EmailStr
    full_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
    )


class RegisterResponse(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str

    @field_validator("username")
    def validate_username(value):
        if len(value) < 5:
            raise ValueError("Username should atleast contain 5 characters")
        return value

    @field_validator("password")
    def validate_password(value):
        if len(value) < 5:
            raise ValueError("Password should atleast contain 5 characters")
        return value

    @field_validator("full_name")
    def validate_fullname(value):
        if len(value) < 3:
            raise ValueError("Password should atleast contain 5 characters")
        return value


class AuthResponse(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_username_or_email(self):

        if self.username is None and self.email is None:
            raise ValueError("Either username or email must be provided")
        return self


class AccessTokenModel(BaseModel):
    access_token: str
    error: Optional[str] = None
