from queue import Queue, Full

from sse.util import MessageSSE


class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self) -> Queue:
        q = Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg: MessageSSE):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except Full:
                del self.listeners[i]


announcer = MessageAnnouncer()
