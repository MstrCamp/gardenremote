from typing import NewType, Dict
from enum import Enum
import json

MessageSSE = NewType("MessageSSE", str)


class MessageType(Enum):
    SENSOR = 1
    RELAY = 2


def format_sse(data: str, event=None) -> MessageSSE:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return MessageSSE(msg)


def dataToJson(mtype: MessageType, content: Dict):
    return json.dumps({
        "type": mtype.name,
        "content": content
    })
