from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import json
from db_map import DatabaseMapper
from bot_states import Grades
from keyboards import Buttons, Keyboard
from aiogram.utils.markdown import text, bold, italic, code, pre
from time import sleep

db = DatabaseMapper()

key = json.load(open('config.json'))['key']
print(key)
bot = Bot(token=key)

dp = Dispatcher(bot, storage=MemoryStorage())

''' For menu '''


@dp.message_handler(commands=['help', 'start'], state='*')
async def hello(message: types.Message):
    await message.answer('''
        Привет! Этот бот поможет тебе узнать куда ты можешь поступить!''',
                         reply_markup=Keyboard.home)
    db.create_user(message.from_user.id)


@dp.message_handler(Text(equals='Назад', ignore_case=True), state='*')
async def get_grades(message: types.Message, state: FSMContext):
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
    grades = '\n'.join(db.get_grades(message.from_user.id))
    if not grades:
        await message.answer("У вас нет оценок.")
    else:
        await message.answer('\n'.join(db.get_grades(message.from_user.id)))

''' Working with grades '''


@dp.callback_query_handler(Text(startswith='st'), state='*')
async def set_zno_grade(callback_query: types.CallbackQuery, state: FSMContext):
    subject = callback_query.data.split('st')[1]

    '''Change state for adding grade'''
    async with state.proxy() as data:
        data['subject'] = subject

    await Grades.grade.set()
    await callback_query.answer()
    await callback_query.message.answer(f'Введите балл по предмету: {subject}\nДля удаления введите 0',
                                        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад')))

''' setting grade and finish state '''


@dp.message_handler(state=Grades.grade)
async def math(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        try:
            data['grade'] = float(message.text)

            if (data['grade'] >= 100 and data['grade'] <= 200) or data['grade'] == 0:
                await message.answer(db.set_grade(
                    message.from_user.id, {'name': data['subject'], 'grade': data['grade']}),
                    reply_markup=Keyboard.home)
                await state.finish()

            else:
                raise ValueError

        except ValueError:
            await message.answer('Некорректное значение')

''' choose area '''


@dp.message_handler(Text(equals='Куда я могу поступить?', ignore_case=True), state='*')
async def get_grades(message: types.Message):

    await message.answer("Выберите область знаний:",
                         reply_markup=Buttons.select_area)
    await Grades.choose_area.set()


@dp.callback_query_handler(state=Grades.choose_area)
async def choose_area(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['area'] = callback_query.data
    await callback_query.message.edit_text('Выберите специальность')
    await callback_query.message.edit_reply_markup(Buttons.gen_specs(callback_query.data))
    await Grades.choose_spec.set()
    await callback_query.answer()


@dp.callback_query_handler(state=Grades.choose_spec)
async def choose_spec(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'all':
        async with state.proxy() as data:
            abilities = db.grades_for_spec(
                tgid=callback_query.from_user.id, area=data['area'])
        nl = '\n'
        message = f"*Вы можете поступить на бюджет:*\n{nl.join(abilities['budget'])}\n\n*На контракт:*\n{nl.join(abilities['contract'])}"
        await callback_query.message.answer(message, parse_mode=types.ParseMode.MARKDOWN)
    elif callback_query.data == 'back':
        await callback_query.message.edit_text('Выберите область')
        await callback_query.message.edit_reply_markup(Buttons.select_area)
        await Grades.choose_area.set()
    else:
        await callback_query.message.answer(db.grades_for_spec(
            tgid=callback_query.from_user.id, spec=callback_query.data))
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
