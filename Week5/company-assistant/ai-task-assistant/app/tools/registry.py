from app.tools.task_tools import create_task_tool, list_tasks_tool
from app.tools.user_tools import get_user_tool
from app.tools.weather_tools import get_weather_tool


TOOL_FUNCTIONS = {
    "get_user": get_user_tool,
    "create_task": create_task_tool,
    "list_tasks": list_tasks_tool,
    "get_weather": get_weather_tool,
}