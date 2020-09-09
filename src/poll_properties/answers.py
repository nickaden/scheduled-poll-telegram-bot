from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from edit_poll import edit_poll_dashboard
from statics import ANSWERS_TYPE, SET_ANSWERS, ANSWERS_CALLBACK


def resolve_answers(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ANSWERS_TYPE, parse_mode=ParseMode.MARKDOWN_V2)
    return SET_ANSWERS


def set_answers(update: Update, context: CallbackContext):
    open_polls = poll_repository.get_open_polls(update.effective_chat.id)
    active_poll = open_polls[0]
    active_poll.answers = update.effective_message.text.splitlines()
    poll_repository.update_poll_entry(active_poll.id, active_poll)
    return edit_poll_dashboard(active_poll, update, context)


answers_callback_handler = CallbackQueryHandler(resolve_answers, pattern=f"^({ANSWERS_CALLBACK})$")
