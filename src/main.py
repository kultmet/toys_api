from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.toys.routers import toy_router

origins = ["*"]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

excluded_routes = ["/status", "/docs", "/openapi.json", "/redoc", "/token"]

app = FastAPI(title="Детский Мир API", middleware=middleware)

app.include_router(toy_router)
