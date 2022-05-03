from aiogram import types

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add('Тренировка')
default_keyboard.add('ℹ️ Информация', '⚙️ Настроить')

settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.add('🕘 Выбрать интервал', '📚 Выбрать предмет')
settings_keyboard.add('◀️ Назад')

cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add('◀️ Отменить')

training_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
training_keyboard.add('▶ Вперёд')
training_keyboard.add('🔚 Закончить')
