from aiogram.dispatcher.filters.state import State, StatesGroup

class Grades(StatesGroup):
    grade = State()
