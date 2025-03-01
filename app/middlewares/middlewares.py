from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.lib.jwt import JwtService


class AuthMiddlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # excluding /auth route
            if request.url.path.startswith("/auth"):
                return await call_next(request)

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=403, content={"error": "Missing authorized token"}
                )

            token = auth_header.split("Bearer ")[1]

            is_verified = JwtService.verify_token(token)
            print("Veritification status->", is_verified)
            if is_verified["payload"] is None:
                return JSONResponse(
                    status_code=403, content={"error": is_verified["error"]}
                )

            return await call_next(request)

        except Exception as e:

            return JSONResponse(content={"error": f"{str(e)}"}, status_code=500)
