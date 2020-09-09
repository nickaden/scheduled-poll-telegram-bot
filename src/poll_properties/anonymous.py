from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from edit_poll import edit_poll_dashboard
from statics import YES, NO, SET_ANONYMOUS, IS_ANONYMOUS_CALLBACK


def resolve_anonymous(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Сделать опрос анонимным?",
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[YES, NO]]))
    return SET_ANONYMOUS


def set_anonymous(update: Update, context: CallbackContext):
    anonymous_answer = update.effective_message.text
    open_polls = poll_repository.get_open_polls(update.effective_chat.id)
    active_poll = open_polls[0]
    active_poll.is_anonymous = anonymous_answer == YES
    poll_repository.update_poll_entry(active_poll.id, active_poll)
    return edit_poll_dashboard(active_poll, update, context)


anonymous_callback_handler = CallbackQueryHandler(resolve_anonymous, pattern=f"^({IS_ANONYMOUS_CALLBACK})$")
