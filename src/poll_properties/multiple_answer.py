from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from edit_poll import edit_poll_dashboard
from statics import YES, NO, IS_MULTIPLE_CALLBACK, SET_MULTIPLE


def resolve_multiple(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Сделать возможность множественного ответа?",
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[YES, NO]]))
    return SET_MULTIPLE


def set_multiple(update: Update, context: CallbackContext):
    multiple_answer = update.effective_message.text
    open_polls = poll_repository.get_open_polls(update.effective_chat.id)
    active_poll = open_polls[0]
    active_poll.is_multiple = multiple_answer == YES
    poll_repository.update_poll_entry(active_poll.id, active_poll)
    return edit_poll_dashboard(active_poll, update, context)


multiple_callback_handler = CallbackQueryHandler(resolve_multiple, pattern=f"^({IS_MULTIPLE_CALLBACK})$")

