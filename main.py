import asyncio
import multiprocessing
import time

import uvicorn

from app.api import app
from tg_bot.bot import start_bot


def run_bot():
    """Запуск ТГ бота"""
    asyncio.run(start_bot())


def run_api():
    """Запуск fastapi"""
    uvicorn.run(app, port=8000)


def watchdog(target, *args):
    """Проверка на работоспособность процессов"""
    while True:
        process = multiprocessing.Process(target=target, args=args)
        process.start()
        process.join()
        if process.exitcode != 0:
            print(f'Процесс "{target.__name__}" завершился с кодом: "{process.exitcode}". Перезапускаю его...')
        time.sleep(5)


if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=watchdog, args=(run_bot,))
    api_process = multiprocessing.Process(target=watchdog, args=(run_api,))

    bot_process.start()
    api_process.start()

    bot_process.join()
    api_process.join()
