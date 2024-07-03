from fastapi import FastAPI

from main.controllers import auth, chat, users
from main.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(chat.router)

    @app.get("/")
    async def index():
        return "Hello World"

    Base.metadata.create_all(engine)

    return app


app = create_app()
