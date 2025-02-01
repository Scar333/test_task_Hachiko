from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from check_imei import CheckIMEI
from config import CONFIG
from .keyboards import get_keyboard
from other import is_valid_imei
from .user_state import UserState

bot = Bot(token=CONFIG['API_TOKEN_TG'])
dp = Dispatcher(storage=MemoryStorage())


# TODO: Команда /start
@dp.message(StateFilter(None), Command("start"))
async def command_start(message: Message) -> None:
    """
    Обработчик команды "/start".

    Args:
        message (Message): Объект сообщения.

    Returns:
        None
    """

    if str(message.from_user.id) in CONFIG['WHITE_LIST']:
        await message.answer(
            text=f'Привет! 🤗'
                 '\n\n'
                 'Этот бот поможет проверить IMEI устройства!',
            reply_markup=get_keyboard()
        )
    else:
        await message.answer(
            text='Извините, у вас нет доступа к данному боту!',
            reply_markup=None
        )


# TODO: Кнопка "Проверить IMEI"
@dp.message(lambda message: message.text == "Проверить IMEI")
async def check_imei(message: Message, state: FSMContext) -> None:
    """
    Обработчик нажатия на кнопку или ручного ввода "Проверить IMEI".

    Args:
        message (Message): Объект сообщения.
        state (FSMContext): Контекст состояния.

    Returns:
        None
    """

    await message.answer(
        text='Введите, пожалуйста, IMEI для проверки:',
        reply_markup=None
    )
    await state.set_state(UserState.waiting_input_new_emei)


# TODO: Ввод IMEI от пользователя
@dp.message(StateFilter(UserState.waiting_input_new_emei))
async def input_imei(message: Message, state: FSMContext):
    """
    Обработчик сообщения ввода IMEI.

    Args:
        message (Message): Объект сообщения.
        state (FSMContext): Контекст состояния.

    Returns:
        None
    """

    if is_valid_imei(imei=message.text):
        id_mess = await message.answer(text='Подождите 10 секунд, обрабатываю данные...')
        await state.update_data(id_mess=id_mess.message_id)

        check_imei_instance = CheckIMEI(imei=message.text)
        info = check_imei_instance.get_data_imei()

        await message.reply(info, reply_markup=get_keyboard())

        data = await state.get_data()
        sent_message_id = data.get('id_mess')
        await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)

        await state.clear()
    else:
        await message.reply("Неверный формат IMEI!"
                            "\n\n"
                            "Повторите попытку ввода.")


# TODO: Запуск бота
async def start_bot() -> None:
    """
    Основная функция для запуска бота.

    Returns:
        None
    """

    await dp.start_polling(bot)
