from typing import List, NewType

MessageSSE = NewType("MessageSSE", str)


def format_sse(data: str, event=None) -> MessageSSE:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return MessageSSE(msg)
