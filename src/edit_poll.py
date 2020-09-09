from telegram import Update, ParseMode, InlineKeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup
from telegram.ext import CallbackContext
import poll_repository
from statics import INFO_DASHBOARD_PATTERN, QUESTION_CALLBACK, ANSWERS_CALLBACK, \
    IS_ANONYMOUS_CALLBACK, IS_MULTIPLE_CALLBACK, SCHEDULE_CALLBACK, EDIT_POLL
from util import format_poll_data

edit_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Question", callback_data=QUESTION_CALLBACK),
        InlineKeyboardButton(text="Answers", callback_data=ANSWERS_CALLBACK)
    ],
    [
        InlineKeyboardButton(text="Is anonymous", callback_data=IS_ANONYMOUS_CALLBACK),
        InlineKeyboardButton(text="Is multiple?", callback_data=IS_MULTIPLE_CALLBACK),
        InlineKeyboardButton(text="Schedule poll", callback_data=SCHEDULE_CALLBACK)
    ]
])


def edit_poll_dashboard(poll: poll_repository.Poll, update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я вас понял! Сейчас сделаем!",
        reply_markup=ReplyKeyboardRemove()
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=INFO_DASHBOARD_PATTERN.format(*format_poll_data(poll)),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=edit_reply_keyboard
    )
    return EDIT_POLL
