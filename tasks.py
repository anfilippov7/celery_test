import time
from celery import Celery


app = Celery(broker='redis://127.0.0.1/1', backend='redis://127.0.0.1/2')

@app.task
def cpu_bound(a):

    time.sleep(1)
    return a