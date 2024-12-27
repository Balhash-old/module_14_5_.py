from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions_14_5 import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


kb1 = InlineKeyboardMarkup(resize_keyboard=True)

button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.add(button3)
kb1.add(button4)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button_ = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb2.insert(button_)
kb2.insert(button_2)
kb2.insert(button_3)
kb2.insert(button_4)
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button)
kb.add(button2)
kb.add(button3)
kb.add(button4)
initiate_db()
check_and_populate_products()
products = get_all_products()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит)')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Регистрация прошла успешно')


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for product in products:
        id_, title, description, price = product
        img_path = f'files/{id_}.png'
        with open(f'{img_path}', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}p')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий Вашему здоровью.'
                         '\nНажмите на кнопку "Рассчитать"', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        'для мужчин 10 х вес (кг)+ 6,25 x рост (см)– 5 х возраст(г) + 5,'
        '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.answer('Введите свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=float(message.text))
    except ValueError:
        await message.answer('Введите свой возраст (сколько Вам полных лет)')
        await UserState.growth.set()
    else:
        await message.answer('Введите свой рост (см)')
        await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=float(message.text))
    except ValueError:
        await message.answer('Введите свой рост (см)')
        await UserState.weight.set()
    else:
        await message.answer('Введите свой вес (кг)')
        await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight=float(message.text))
    except ValueError:
        await message.answer('Введите свой вес (кг)')
        await UserState.weight.set()
    else:
        data = await state.get_data()
        result = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
        await message.answer(f'Ваша норма калорий {result} в день. Спасибо, что обратились к нам!  ')
        await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение !')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
