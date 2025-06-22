from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handler for the /start command."""
    await message.answer(
        "Здравствуйте! Я бот для сбора 360-градусного фидбэка. \n"
        "Для получения списка команд, введите /help."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handler for the /help command."""
    # TODO: Добавить ролевую модель (HR-админ / респондент)
    help_text = (
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Показать это сообщение\n"
        "/status - Показать статус активных циклов сбора фидбэка"
    )
    await message.answer(help_text)

@router.message(Command("status"))
async def cmd_status(message: Message):
    """Handler for the /status command."""
    # TODO: Реализовать логику получения статуса из хранилища
    await message.answer("Активных циклов нет.")
