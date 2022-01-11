from aiogram.dispatcher.filters.state import State, StatesGroup

class Grades(StatesGroup):
    math = State()
    mova = State()
    mova_lit = State()
    history = State()
    biology = State()
    lang = State()
    chemistry = State()
    physics = State()
    geography = State()
    attestat = State()

    mods = {'Математика':math,'Українська мова':mova,
            'Історія України':history,'Іноземна мова':lang,
            'Біологія':biology,'Хімія':chemistry,
            'Фізика':physics,'Географія':geography,
            'Середній бал документа про освіту':attestat}