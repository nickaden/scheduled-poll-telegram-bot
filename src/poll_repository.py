import json
from dataclasses import dataclass
from typing import List
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr, Key

table = boto3.resource("dynamodb").Table("polls")


@dataclass
class Poll:
    id: str
    chat_id: int
    question: str
    answers: List
    is_anonymous: bool
    is_multiple: bool
    schedule: str
    status: str


def get_open_polls(chat_id) -> List[Poll]:
    result = table.scan(FilterExpression=Attr('chat_id').eq(chat_id) & Attr("status").eq("OPEN"))
    if len(result["Items"]) > 1:
        raise Exception("Too much open polls")
    if result["Items"]:
        return [Poll(id=entry["poll_id"],
                     chat_id=entry["chat_id"],
                     question=entry["question"],
                     answers=json.loads(entry.get("answers")) if entry["answers"] else [],
                     is_anonymous=entry["is_anonymous"],
                     is_multiple=entry["is_multiple"],
                     schedule=entry["schedule"],
                     status=entry["status"]) for entry in result["Items"]]
    else:
        return []


def get_polls_by_id(poll_id) -> Poll:
    result = table.query(KeyConditionExpression=Key("chat_id").eq(poll_id))
    if result["Items"] and len(result["Items"]) == 1:
        entry = result["Items"][0]
        return Poll(id=entry["poll_id"],
                    chat_id=entry["chat_id"],
                    question=entry["question"],
                    answers=json.loads(entry["answers"]),
                    is_anonymous=entry["is_anonymous"],
                    is_multiple=entry["is_multiple"],
                    schedule=entry["schedule"],
                    status=entry["status"])
    else:
        return None


def create_new_poll_entry(chat_id, question=None, answers=None,
                          is_anonymous=True, is_multiple=False, schedule=None):
    poll_id = str(uuid4())
    table.put_item(Item={
        "poll_id": poll_id,
        "chat_id": chat_id,
        "question": question,
        "answers": answers or json.dumps([]),
        "is_anonymous": is_anonymous,
        "is_multiple": is_multiple,
        "schedule": schedule,
        "status": "OPEN",
    })
    return Poll(id=poll_id, chat_id=chat_id, question=question, answers=answers or [], is_anonymous=is_anonymous,
                is_multiple=is_multiple,
                schedule=schedule, status="OPEN")


def update_poll_entry(poll_id, poll: Poll):
    table.update_item(
        Key={"poll_id": poll_id},
        UpdateExpression="SET chat_id = :chat_id, question = :question, answers = :answers, \
                        is_anonymous = :is_anonymous, is_multiple = :is_multiple, schedule = :schedule, #st = :st",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={
            ":chat_id": poll.chat_id,
            ":question": poll.question,
            ":answers": json.dumps(poll.answers),
            ":is_anonymous": poll.is_anonymous,
            ":is_multiple": poll.is_multiple,
            ":schedule": poll.schedule,
            ":st": poll.status
        }
    )


def delete_poll(poll_id):
    table.delete_item(Key={"poll_id": poll_id})
