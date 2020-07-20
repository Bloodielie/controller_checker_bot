from aiogram import types

from app.keybords.raw_text import city_raw_text, representation_raw_text


def start_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(*[types.KeyboardButton(text) for text in city_raw_text(locale)])
    return keyboard_markup


def representation_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(*[types.KeyboardButton(text) for text in representation_raw_text(locale)])
    return keyboard_markup


def menu_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard_markup.add(types.KeyboardButton(locale.get_updates))
    keyboard_markup.add(types.KeyboardButton(locale.settings))
    # keyboard_markup.add(types.KeyboardButton(locale.about_project))
    return keyboard_markup


def settings_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard_markup.add(types.KeyboardButton(locale.settings_city))
    keyboard_markup.add(types.KeyboardButton(locale.settings_representation))
    keyboard_markup.add(types.KeyboardButton(locale.settings_number_of_posts))
    keyboard_markup.add(types.KeyboardButton(locale.back))
    return keyboard_markup


def settings_representation_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(*[types.KeyboardButton(text) for text in representation_raw_text(locale)])
    keyboard_markup.add(types.KeyboardButton(locale.back))
    return keyboard_markup


def settings_city_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(*[types.KeyboardButton(text) for text in city_raw_text(locale)])
    keyboard_markup.add(types.KeyboardButton(locale.back))
    return keyboard_markup


def settings_number_of_posts_keyboard(locale):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(*[types.KeyboardButton(number) for number in locale.number_of_posts])
    keyboard_markup.add(types.KeyboardButton(locale.back))
    return keyboard_markup
