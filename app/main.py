from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.assistants import router as assistants_router

app = FastAPI(title="FastAPI + Docker + Alembic")

app.include_router(users_router)
app.include_router(assistants_router)