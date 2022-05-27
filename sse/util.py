import json
from enum import Enum
from typing import NewType, Dict

MessageSSE = NewType("MessageSSE", str)


class MessageType(Enum):
    SENSOR = 1
    RELAY = 2
    SHUTTER = 3


def format_sse(data: str, event=None) -> MessageSSE:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return MessageSSE(msg)


def dataToJson(mtype: MessageType, content: Dict) -> str:
    return json.dumps({
        "type": mtype.name,
        "content": content
    })
