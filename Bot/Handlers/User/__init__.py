from aiogram import Router

from .handler import UserHandler


def User_handler_router() -> Router:
    router = Router()

    UserHandler(router=router)

    return router
