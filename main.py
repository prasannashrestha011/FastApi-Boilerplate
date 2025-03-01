from fastapi import FastAPI
from dotenv import load_dotenv
from app.middlewares.middlewares import AuthMiddlware

load_dotenv()
# app routes
from app.routes.AuthRoute import router as auth_routes
from app.routes.HomeRoute import router as home_routes

app = FastAPI()

app.add_middleware(AuthMiddlware)

app.include_router(home_routes)
app.include_router(auth_routes)
