import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import settings
from src.handlers import common
from src.services.google_sheets import google_sheets_service

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """Основная функция для запуска бота."""
    # Проверка наличия токена
    if not settings.BOT_TOKEN:
        logger.critical("Ошибка: BOT_TOKEN не найден. Проверьте ваш .env файл.")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN)
    # Используем MemoryStorage для начала, позже заменим на Redis
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    logger.info(f"Бот запускается в среде: {settings.ENVIRONMENT}")

    # Регистрируем роутеры
    dp.include_router(common.router)

    # Проверяем подключение к Google Sheets при старте
    logger.info("Проверка подключения к Google Sheets...")
    employees = google_sheets_service.get_employees()
    if employees is None:
        logger.error("Не удалось получить данные из Google Sheets. Проверьте настройки и права доступа.")
        # В зависимости от критичности, можно либо остановить бота, либо продолжить работу с ограниченным функционалом
    else:
        logger.info("Подключение к Google Sheets успешно.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
