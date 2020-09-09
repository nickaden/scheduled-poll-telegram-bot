from telegram import Update
from telegram.ext import Updater, CommandHandler, Dispatcher, CallbackContext, ConversationHandler, MessageHandler, \
    Filters
import os
import logging

from commit_options.save_poll import save_poll_callback_handler
from poll_properties.anonymous import set_anonymous, anonymous_callback_handler
from poll_properties.answers import set_answers, answers_callback_handler
from create_poll_management import check_open_polls, get_or_create_poll_handler
from poll_properties.multiple_answer import set_multiple, multiple_callback_handler
from poll_properties.question import set_question, question_callback_handler
from poll_properties.schedule import set_schedule, schedule_callback_handler
from statics import START_MESSAGE, SELECT_POLL, EDIT_POLL, COMMIT_CHANGES, SET_QUESTION, SET_ANSWERS, SET_ANONYMOUS, \
    SET_MULTIPLE, SET_SCHEDULE

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=START_MESSAGE)


def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="User canceled poll creation")


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler("newPoll", check_open_polls)],
        states={
            SELECT_POLL: [
                get_or_create_poll_handler
            ],
            EDIT_POLL: [
                question_callback_handler,
                answers_callback_handler,
                anonymous_callback_handler,
                multiple_callback_handler,
                schedule_callback_handler
            ],
            COMMIT_CHANGES: [
                save_poll_callback_handler
            ],
            SET_QUESTION: [MessageHandler(Filters.text & (~Filters.command), set_question)],
            SET_ANSWERS: [MessageHandler(Filters.text & (~Filters.command), set_answers)],
            SET_ANONYMOUS: [MessageHandler(Filters.text & (~Filters.command), set_anonymous)],
            SET_MULTIPLE: [MessageHandler(Filters.text & (~Filters.command), set_multiple)],
            SET_SCHEDULE: [MessageHandler(Filters.text & (~Filters.command), set_schedule)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    ))

    updater.start_polling()


if __name__ == '__main__':
    main()
