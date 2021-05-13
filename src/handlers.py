import os
from tempfile import NamedTemporaryFile
from telebot import TeleBot, logger, types
from .config import get_config, WELLCOME_MESSAGE, HELP_MESSAGE
from .mri_controller import MriController

token, admin_users = get_config()
bot = TeleBot(token)

controller = MriController()

for admin in admin_users:
    bot.send_message(admin, 'Initialized.')

lock = False


def is_typing_dec(f):
    def _internal_f(message: types.Message):
        bot.send_chat_action(message.chat.id, 'typing')
        return f(message)

    return _internal_f


def one_command_lock(f):
    def _internal_f(message: types.Message):
        global lock
        if lock:
            bot.reply_to(message, 'Wait, Im bussy.')
            return
        lock = True
        res = f(message)
        lock = False
        return res

    return _internal_f


def one_query_lock(f):
    def _internal_f(call):
        global lock
        if lock:
            bot.send_message(call.message.chat.id, 'Wait, Im bussy.')
            return
        lock = True
        res = f(call)
        lock = False
        return res

    return _internal_f


@is_typing_dec
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.reply_to(message, WELLCOME_MESSAGE % (message.from_user.first_name))
    help(message)


@is_typing_dec
@bot.message_handler(commands=['choose_dataset'])
@one_command_lock
def change_dataset(message: types.Message):
    bot.send_chat_action(message.chat.id, 'typing')
    markup = types.InlineKeyboardMarkup()
    for ds in controller.datasets:
        if ds is None or ds == '':
            continue
        item = types.InlineKeyboardButton(text=ds, callback_data='dataset:%s' % ds)
        markup.row(item)
    bot.send_message(message.chat.id, 'Choose a dataset:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'dataset' in call.data)
@one_query_lock
def use_dataset(call):
    ds = call.data.split(':')[1]
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Please wait...')
    if controller.change_dataset(name=ds):
        bot.send_message(chat_id, 'Dataset loaded.')
    else:
        bot.send_message(chat_id, 'I can\'t find the dataset "%s".' % (ds))


@is_typing_dec
@bot.message_handler(commands=['activate_roccio'])
@one_command_lock
def activate_roccio(message: types.Message):
    controller.set_roccio(activated=True)
    bot.send_message(message.chat.id, 'Activated roccio on queries')


@is_typing_dec
@bot.message_handler(commands=['deactivate_roccio'])
@one_command_lock
def deactivate_roccio(message: types.Message):
    controller.set_roccio(activated=False)
    bot.send_message(message.chat.id, 'Deactivated roccio on queries')


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
    bot.send_sticker(
        message.chat.id,
        'CAACAgQAAxkBAAOCYJTZ6sgxXMjiyaFE5kM8cvf3mF0AAkwWAAKm8XEezNf5LuZMOxYfBA',
    )


@is_typing_dec
@bot.message_handler(func=lambda m: m.text[0] != '/')
@one_command_lock
def default_search(message: types.Message):
    bot.send_message(message.chat.id, 'Please wait...')
    docs: list = controller.execute_query(message.text)
    if docs:
        # build response
        response = 'Results:'
        response = response + '\n\n'
        response = response + '\n\n'.join(
            [" *%s*. ``` %s ```" % (i + 1, repr(d)) for i, d in enumerate(docs)]
        )
        response = response + '\n'

        # build downloads Buttons
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i, d in enumerate(docs):
            item = types.InlineKeyboardButton(
                text='download %d. \n%s \n%s ' % (i + 1, d.title, d.author),
                callback_data='download:%s' % (d.id),
            )
            markup.row(item)

        # send message
        bot.send_message(
            message.chat.id, response, parse_mode="Markdown", reply_markup=markup
        )
    else:
        bot.send_message(
            message.chat.id,
            'Can\'t find anything, you may need to configure the dataset.',
        )


@bot.callback_query_handler(func=lambda call: 'download' in call.data)
# @one_query_lock
def handle_download_query(call):
    id = call.data.split(":")[1]
    chat_id = call.message.chat.id
    doc_json = controller.get_document_json(id)
    if doc_json is None:
        bot.send_message(
            chat_id,
            'Can\'t find a document with id(%s) in the current dataset.' % (id),
        )
    else:
        bot.send_chat_action(chat_id, 'upload_document')
        f = NamedTemporaryFile(
            mode='w+', delete=False, prefix=f'doc{id}_', suffix='.json'
        )
        f.write(doc_json)
        f.close()
        with open(f.name, "rb") as nf:
            bot.send_document(chat_id, nf)
        os.unlink(f.name)  # delete the file after

