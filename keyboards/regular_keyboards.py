from aiogram import types

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add('ℹ️ Информация', '⚙️ Настроить')

settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.add('🕘 Выбрать интервал', '📚 Выбрать предмет')
settings_keyboard.add('◀️ Назад')

cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add('◀️ Отменить')

# TODO
available_subjects = ['Обществознание']

subject_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
subject_keyboard.add(*available_subjects)
