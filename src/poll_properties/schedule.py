from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CallbackQueryHandler

import poll_repository
from edit_poll import edit_poll_dashboard
from statics import SCHEDULE_CRON_REQUEST_TEXT, SET_SCHEDULE, SCHEDULE_CALLBACK


def resolve_schedule(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=SCHEDULE_CRON_REQUEST_TEXT,
                             parse_mode=ParseMode.MARKDOWN_V2)
    return SET_SCHEDULE


def set_schedule(update: Update, context: CallbackContext):
    schedule_cron = update.effective_message.text
    active_poll = poll_repository.get_open_polls(update.effective_chat.id)[0]
    active_poll.schedule = schedule_cron
    poll_repository.update_poll_entry(active_poll.id, active_poll)
    return edit_poll_dashboard(active_poll, update, context)


schedule_callback_handler = CallbackQueryHandler(resolve_schedule, pattern=f"^({SCHEDULE_CALLBACK})$")
