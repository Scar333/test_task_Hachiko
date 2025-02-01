from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    """
    Состояния для процесса обработки пользователя.

    Attributes:
        waiting_input_new_emei (State): Состояние ожидания ввода нового emei.
    """
    waiting_input_new_emei = State()
