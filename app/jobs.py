
@scheduler.task('interval', id='do_job_1', minutes=5, misfire_grace_time=900)
def job1():
    announcer.announce(format_sse("test from interval job"))
    print('Job 1 executed')
