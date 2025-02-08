from aiogram import Router
from .handlers.commands.start import start_router



main_router = Router()

main_router.include_router(start_router)