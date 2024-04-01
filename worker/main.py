import time

import schedule

from database import get_session
from database.models import DBTask


def run_get_tasks():
    with get_session() as session:
        tasks = session.query(DBTask).all()


schedule.every().minute.at(":00").do(run_get_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)
