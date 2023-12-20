from bot.database.methods.create import create_table_users


def register_models() -> None:
    create_table_users()
