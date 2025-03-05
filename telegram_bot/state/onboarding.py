from aiogram.fsm.state import State, StatesGroup


class OnboardingState(StatesGroup):
    amount = State()
    amount_sell = State()
