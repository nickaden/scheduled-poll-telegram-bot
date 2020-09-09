from telegram import Update, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import poll_repository
from statics import INFO_DASHBOARD_PATTERN, COMMIT_CHANGES, DELETE_CALLBACK, EDIT_CALLBACK, SAVE_CALLBACK
from util import format_poll_data

commit_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Save", callback_data=SAVE_CALLBACK),
        InlineKeyboardButton(text="Edit", callback_data=EDIT_CALLBACK),
        InlineKeyboardButton(text="Delete", callback_data=DELETE_CALLBACK)
    ]
])


def commit_changes_dashboard(poll: poll_repository.Poll, update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я вас понял! Сейчас сделаем!",
        reply_markup=ReplyKeyboardRemove()
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=INFO_DASHBOARD_PATTERN.format(*format_poll_data(poll)),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=commit_reply_keyboard
    )

    return COMMIT_CHANGES
