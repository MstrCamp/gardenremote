from sse.MessageAnnouncer import announcer
from sse.util import format_sse
from . import scheduler

i: int = 0


@scheduler.task('interval', id='do_job_1', minutes=5, misfire_grace_time=900)
def job1():
    global i
    announcer.announce(format_sse(f"test {i} from interval job"))
    i += 1
