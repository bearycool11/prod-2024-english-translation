from functools import wraps


def task(func):
    from database import get_session

    @wraps(func)
    def wrapper(*args, **kwargs):
        task_model = kwargs.pop("task")
        with get_session() as session:
            session.delete(task_model)
            session.commit()
        return func(*args, **kwargs)

    return wrapper
