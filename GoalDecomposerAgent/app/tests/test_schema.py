def main() -> None:
    from sqlalchemy import inspect
    from app.core.database import engine
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        for column in inspector.get_columns(table_name):
            print("  -", column["name"])


if __name__ == "__main__":
    main()
