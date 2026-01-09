from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.assistants import router as assistants_router
from app.api.chats import router as chats_router
from app.api.messages import router as messages_router

app = FastAPI(title="FastAPI + Docker + Alembic")

app.include_router(users_router)
app.include_router(assistants_router)
app.include_router(chats_router)
app.include_router(messages_router)
