from aiogram import Router

from .handler import AdminHandler


def Admin_handler_router() -> Router:
    router = Router()

    AdminHandler(router=router)

    return router
