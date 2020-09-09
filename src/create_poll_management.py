from telegram import Update, ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters

import poll_repository
from commit_changes import commit_changes_dashboard
from edit_poll import edit_poll_dashboard
from statics import OPEN_POLL_QUESTION, YES, NO, SELECT_POLL


def check_open_polls(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    open_polls = poll_repository.get_open_polls(chat_id)
    if open_polls:
        context.bot.send_message(
            chat_id=chat_id,
            text=OPEN_POLL_QUESTION.format(open_polls[0].question),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=ReplyKeyboardMarkup(keyboard=[[YES, NO]])
        )
        return SELECT_POLL
    else:
        poll = poll_repository.create_new_poll_entry(update.effective_chat.id)
        return edit_poll_dashboard(poll, update, context)


def get_or_create_poll(update: Update, context: CallbackContext):
    text = update.effective_message.text
    open_polls = poll_repository.get_open_polls(update.effective_chat.id)
    if text == YES:
        return poll_dashboard(open_polls[0], update, context)
    else:
        for poll in open_polls:
            poll_repository.delete_poll(poll.id)
        poll = poll_repository.create_new_poll_entry(update.effective_chat.id)
        return edit_poll_dashboard(poll, update, context)


def poll_dashboard(poll, update, context):
    if poll.question and poll.answers and poll.schedule:
        return commit_changes_dashboard(poll, update, context)
    else:
        return edit_poll_dashboard(poll, update, context)


get_or_create_poll_handler = MessageHandler(Filters.regex("^(Да|Нет)$"), get_or_create_poll)
