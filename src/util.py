from cron_descriptor import Options, ExpressionDescriptor

from poll_repository import Poll


def format_poll_data(poll: Poll):
    options = Options()
    options.locale_code = "ru_RU"
    return (
        poll.question or "Нет",
        ("\n\t\\- " + "\n\t\\- ".join(poll.answers)) if poll.answers else "Нет",
        "Да" if poll.is_anonymous else "Нет",
        "Да" if poll.is_multiple else "Нет",
        str(ExpressionDescriptor(poll.schedule, options)) if poll.schedule else "Не установлено"
    )
