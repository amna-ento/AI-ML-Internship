from app.services.task_service import create_task, list_tasks


def create_task_tool(user_id: int, title: str):
    try:
        return create_task(user_id, title)
    except ValueError as error:
        return {"error": str(error)}


def list_tasks_tool(user_id: int):
    try:
        return list_tasks(user_id)
    except ValueError as error:
        return {"error": str(error)}