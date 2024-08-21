def create_name_todo_table(user_id: int) -> str:
    """Названия таблицы с данными о задачах"""
    table_name = f"todo_{user_id}"
    return table_name
