from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import requests
import json
from db_map import DatabaseMapper
from bot_states import Grades
from keyboards import Buttons, Keyboard
from time import sleep

db = DatabaseMapper()

key = json.load(open('config.json'))['key']
print(key)
bot = Bot(token=key)

dp = Dispatcher(bot,storage=MemoryStorage())

''' For menu '''

@dp.message_handler(commands=['help','start'], state='*')
async def hello(message: types.Message):
    await message.answer('''
        Привет! Этот бот поможет тебе узнать куда ты можешь поступить!''',
        reply_markup=Keyboard.home)
    db.create_user(message.from_user.id)
    
@dp.message_handler(Text(equals='Назад', ignore_case=True), state='*')
async def get_grades(message: types.Message,state: FSMContext):
    await message.answer('Возвращаемся назад...',
        reply_markup=Keyboard.home)
    await state.finish()

''' Choose method '''

@dp.message_handler(Text(equals='Добавить оценки ЗНО', ignore_case=True), state='*')
async def get_grades(message: types.Message):
    msg = await message.answer('Выберите предмет:',
                        reply_markup=Buttons.select_zno)



@dp.message_handler(Text(equals='Мои баллы', ignore_case=True), state='*')
async def get_grades(message: types.Message):
    await message.answer('\n'.join(db.get_grades(message.from_user.id)))
    
''' Add grades for user '''

@dp.callback_query_handler(Text(startswith='st'))
async def set_zno_grade(callback_query: types.CallbackQuery):
    print(callback_query.data)
    subject = callback_query.data.split('st')[1]

    '''Change state for adding grade'''

    await Grades.mods[subject].set()   
    await callback_query.message.answer(f'Введите балл по предмету: {subject}')


@dp.message_handler(state=Grades.math)
async def math(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['name'] = 'Математика'
        data['grade'] = float(message.text)

        if message.text.isdigit():

            if data['grade']>=100 and data['grade'] >=100:
                await message.answer(f'Ваша оцiночка {data["grade"]}')
                await state.finish()

            else:
                await message.answer('Некорректное значение')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)