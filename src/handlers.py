from logging import log
from telebot import TeleBot
from telebot import types
from .config import get_config, WELLCOME_MESSAGE, HELP_MESSAGE

token, admin_users = get_config()
bot = TeleBot(token)


def is_typing_dec(f):
    def _internal_f(message):
        bot.send_chat_action(message.chat.id, 'typing')
        return f(message)

    return _internal_f


@is_typing_dec
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, WELLCOME_MESSAGE % (message.from_user.first_name))
    help(message)


@is_typing_dec
@bot.message_handler(commands=['choose_dataset'])
def change_dataset(message):
    bot.send_chat_action(message.chat.id, 'typing')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    itembtcran = types.KeyboardButton('/use_dataset cran')
    itembtcisi = types.KeyboardButton('/use_dataset cisi',)
    markup.row(itembtcran)
    markup.row(itembtcisi)
    bot.send_message(message.chat.id, "Choose a dataset:", reply_markup=markup)


@is_typing_dec
@bot.message_handler(commands=['use_dataset'])
def use_dataset(message):
    # todo: logic to change the dataset
    remove_board = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Done.', reply_markup=remove_board)


@is_typing_dec
@bot.message_handler(commands=['getid'])
def get_id(message: types.Message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, str(user_id))


@is_typing_dec
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['get_report'])
def get_report(message):
    bot.send_chat_action(message.chat.id, 'upload_document')
    doc = open('doc/report.zip', 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAANbYJTVtWS_1zDiWRd-OsbsKVqVmnYAAsEKAAIeYaFKWYvGKswsyeUfBA',
    )


# Handle sticker message
@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
    # (message.sticker.file_id)
    # bot.send_message(message.chat.id, f'{message.sticker.file_id}')
    bot.send_sticker(
        message.chat.id,
        'CAACAgQAAxkBAAOCYJTZ6sgxXMjiyaFE5kM8cvf3mF0AAkwWAAKm8XEezNf5LuZMOxYfBA',
    )


@is_typing_dec
@bot.message_handler(func=lambda m: True)
def default_search(message):
    # todo logic for querie test here
    # bot.send_message(message.chat.id, 'jlkjlj')
    pass


def error(message):
    log('<--error-->')
