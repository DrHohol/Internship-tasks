from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from db_map import DatabaseMapper

class Keyboard():

    button_add = KeyboardButton('Додати оцiнки ЗНО')
    button_my = KeyboardButton('Мои бали')
    button_where = KeyboardButton('Куди я можу поступити?')

    home = ReplyKeyboardMarkup(resize_keyboard=True)
    home.add(button_add, button_my)
    home.add(button_where)


class Buttons():

    znos = DatabaseMapper().all_znos()

    select_zno = InlineKeyboardMarkup(row_width=2)
    for zno in znos:
        ''' Using st bcs of 64byte data limit '''
        select_zno.insert(InlineKeyboardButton(
            text=zno, callback_data=f'st{zno}'))

    areas = DatabaseMapper().all_areas()

    select_area = InlineKeyboardMarkup(row_width=2)
    for area in areas:
        ''' Split for 64byte limit '''
        select_area.insert(InlineKeyboardButton(
            text=area, callback_data=area[0:50]))

    def gen_specs(area):

        specs = DatabaseMapper().specs(area)

        select_spec = InlineKeyboardMarkup(row_width=2)
        for spec in specs:
            ''' Using st bcs of 64byte data limit '''
            select_spec.insert(InlineKeyboardButton(
                text=spec, callback_data=spec[0:30]))
        select_spec.add(InlineKeyboardButton(
                text='Усi спецiальностi', callback_data='all'))
        select_spec.add(InlineKeyboardButton(
                text='Назад', callback_data='back'))

        return select_spec
