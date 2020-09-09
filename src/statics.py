from enum import Enum

START_MESSAGE = "Привет! Чтобы создать новый опрос, используй команду /newPoll"
YES, NO = "Да", "Нет"

INFO_DASHBOARD_PATTERN = """
Ваш текущий опрос:

*Вопрос:* {}
*Ответы:* {} 
*Анонимный:* {}
*Множественный ответ:* {}
*Расписание:* {}

Что будем делать?
"""

OPEN_POLL_QUESTION = """
Вы не закончили создавать опрос с вопросом *{}*

Хотите его завершить?
"""

ANSWERS_TYPE = """
Введите ответы в каждой новой строке:

Пример:
_Да_
_Возможно_
_Нет_
"""

ANONYMOUS = "Опрос предполагает анонимный ответ"
NOT_ANONYMOUS = "Опрос будет публичным"

MULTIPLE = "На опрос можно отвечать несколько раз"
NOT_MULTIPLE = "Опрос будет иметь единственный ответ"

SCHEDULE_CRON_REQUEST_TEXT = """
Ввведите значение CRON для расписания опроса \\(Смотри [справку](https://www.freeformatter.com/cron-expression-generator-quartz.html)\\)
"""

SAVE_COMPLETE = "Опрос успешно сохранен"

SELECT_POLL, EDIT_POLL, SET_QUESTION, SET_ANSWERS, SET_ANONYMOUS, SET_MULTIPLE, SET_SCHEDULE, COMMIT_CHANGES = range(8)

QUESTION_CALLBACK, ANSWERS_CALLBACK, IS_ANONYMOUS_CALLBACK, IS_MULTIPLE_CALLBACK, SCHEDULE_CALLBACK, SAVE_CALLBACK, \
    EDIT_CALLBACK, DELETE_CALLBACK = range(8)
