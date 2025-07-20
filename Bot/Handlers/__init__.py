from aiogram import Router

from Bot.Handlers.User import User_handler_router
from Bot.Handlers.Admin import Admin_handler_router


def Handler_Router() -> Router:
    router = Router()

    """ Место для добавление роутеров"""
    router.include_router(Admin_handler_router())
    router.include_router(User_handler_router())

    return router
