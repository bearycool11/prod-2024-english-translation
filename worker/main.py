import datetime
import threading
import time

import requests
import schedule

import handlers
from database import get_session
from database.models import DBTask, DBOrganizationStopToggle


def run_get_tasks():
    with get_session() as session:
        now_datetime = datetime.datetime.now()
        tasks = session.query(DBTask).filter(DBTask.planned_time <= now_datetime).all()
    for task in tasks:
        try:
            task.arguments.update({"task": task})
            if "organization_id" in task.arguments:
                organization_id = task.arguments.pop("organization_id")
                with get_session() as session:
                    if session.query(DBOrganizationStopToggle).filter(
                            DBOrganizationStopToggle.organization_id == organization_id).count():
                        session.delete(task)
                        session.commit()
                        post_id = task.arguments.pop("post_id")
                        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                                      json={"post_id": post_id, "post_status": "NOT_READY",
                                            "telegram_message_id": None,
                                            "channel_id": None, "chat_username": None, "clear_planned_time": True})
                        continue
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
