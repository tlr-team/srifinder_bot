from logging import log
from telebot import TeleBot
from telebot import types
from .config import get_config, WELLCOME_MESSAGE, HELP_MESSAGE
from .mri_controller import MriController

token, admin_users = get_config()
bot = TeleBot(token)
controller = MriController()


def is_typing_dec(f):
    def _internal_f(message: types.Message):
        bot.send_chat_action(message.chat.id, 'typing')
        return f(message)

    return _internal_f


@is_typing_dec
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.reply_to(message, WELLCOME_MESSAGE % (message.from_user.first_name))
    help(message)


@is_typing_dec
@bot.message_handler(commands=['choose_dataset'])
def change_dataset(message: types.Message):
    bot.send_chat_action(message.chat.id, 'typing')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    for ds in controller.datasets:
        if ds is None or ds == '':
            continue
        item = types.KeyboardButton('/use_dataset %s' % ds)
        markup.row(item)

    bot.send_message(message.chat.id, 'Choose a dataset:', reply_markup=markup)


@is_typing_dec
@bot.message_handler(commands=['use_dataset'])
def use_dataset(message: types.Message):
    ds_c = message.text.split(' ')
    ds = '' if ds_c is None or len(ds_c) <= 1 else ds_c[1]

    if controller.change_dataset(name=ds):
        remove_board = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Dataset loaded.', reply_markup=remove_board)
    else:
        remove_board = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            'I can\'t find the dataset "%s".' % (ds),
            reply_markup=remove_board,
        )


@is_typing_dec
@bot.message_handler(commands=['getid'])
def get_id(message: types.Message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, str(user_id))


@is_typing_dec
@bot.message_handler(commands=['help'])
def help(message: types.Message):
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['get_report'])
def get_report(message: types.Message):
    bot.send_chat_action(message.chat.id, 'upload_document')
    doc = open('doc/report.zip', 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAANbYJTVtWS_1zDiWRd-OsbsKVqVmnYAAsEKAAIeYaFKWYvGKswsyeUfBA',
    )


# Handle sticker message
@bot.message_handler(content_types=['sticker'])
def handle_stickers(message: types.Message):
    # (message.sticker.file_id)
    # bot.send_message(message.chat.id, f'{message.sticker.file_id}')
    bot.send_sticker(
        message.chat.id,
        'CAACAgQAAxkBAAOCYJTZ6sgxXMjiyaFE5kM8cvf3mF0AAkwWAAKm8XEezNf5LuZMOxYfBA',
    )


@is_typing_dec
@bot.message_handler(func=lambda m: True)
def default_search(message: types.Message):
    docs: list = controller.execute_query(message.text)
    if docs:
        response = 'Results:\n\n\t'
        response = response + '\n\n\t'.join(
            ["%s : %s " % (i, d) for i, d in enumerate(docs)]
        )
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(
            message.chat.id,
            'Can\'t find anything, you may need to configure the dataset.',
        )


def error(message: types.Message):
    log('<--error-->')
