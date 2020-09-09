from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from edit_poll import edit_poll_dashboard
from statics import SET_QUESTION, QUESTION_CALLBACK


def resolve_question(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите вопрос:")
    return SET_QUESTION


def set_question(update: Update, context: CallbackContext):
    open_polls = poll_repository.get_open_polls(update.effective_chat.id)
    active_poll = open_polls[0]
    active_poll.question = update.effective_message.text
    poll_repository.update_poll_entry(active_poll.id, active_poll)
    return edit_poll_dashboard(active_poll, update, context)


question_callback_handler = CallbackQueryHandler(resolve_question, pattern=f"^({QUESTION_CALLBACK})$")
