from app.services.user_service import get_user


def get_user_tool(user_id: int):
    try:
        return get_user(user_id)
    except ValueError as error:
        return {"error": str(error)}