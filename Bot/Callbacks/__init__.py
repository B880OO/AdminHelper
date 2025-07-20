from aiogram import Router

from Bot.Callbacks.User import User_callback_router
from Bot.Callbacks.Admin import Admin_callback_router


def Callback_Router() -> Router:
    router = Router()

    """ Место для добавление роутеров """
    router.include_router(User_callback_router())
    router.include_router(Admin_callback_router())

    return router
