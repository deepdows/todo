from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from database import engine
from database_init import Base
from todo.router import router as todo_router
from user.router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)
app.include_router(user_router)
