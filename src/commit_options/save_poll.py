from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from statics import SAVE_COMPLETE, SAVE_CALLBACK


def save_poll(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    open_polls = poll_repository.get_open_polls(chat_id)
    for poll in open_polls:
        poll.status = "COMPLETE"
        poll_repository.update_poll_entry(poll.id, poll)

    context.bot.send_message(chat_id=chat_id, text=SAVE_COMPLETE)
    return -1


save_poll_callback_handler = CallbackQueryHandler(callback=save_poll, pattern=f"^({SAVE_CALLBACK})$")
