from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from db_map import DatabaseMapper

class Keyboard():



    button_add = KeyboardButton('Добавить оценки ЗНО')
    button_my = KeyboardButton('Мои баллы')
    button_where = KeyboardButton('Куда я могу поступить?')

    home = ReplyKeyboardMarkup(resize_keyboard=True)
    home.add(button_add,button_my)
    home.add(button_where)



class Buttons():
    
    znos = DatabaseMapper().all_znos()

    select_zno = InlineKeyboardMarkup(row_width=2,one_time_keyboard=True)
    for zno in znos:
        #print(len(zno.encode('utf-8')))
        select_zno.insert(InlineKeyboardButton(text=zno, callback_data=f'st{zno}'))