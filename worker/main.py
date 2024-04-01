import datetime
import threading
import time

import schedule

import handlers
from database import get_session
from database.models import DBTask


def run_get_tasks():
    with get_session() as session:
        now_datetime = datetime.datetime.now()
        tasks = session.query(DBTask).filter(DBTask.planned_time <= now_datetime).all()
    for task in tasks:
        try:
            task.arguments.update({"task": task})
            thread = threading.Thread(target=getattr(handlers, task.handler), kwargs=task.arguments)
            thread.start()
        except AttributeError:
            # handler not found
            pass
        except:
            # error
            pass


schedule.every().minute.at(":00").do(run_get_tasks)

while True:
    schedule.run_pending()
    time.sleep(0.1)
