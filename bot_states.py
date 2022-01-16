from aiogram.dispatcher.filters.state import State, StatesGroup


class Grades(StatesGroup):
    grade = State()
    choose_area = State()
    choose_spec = State()
