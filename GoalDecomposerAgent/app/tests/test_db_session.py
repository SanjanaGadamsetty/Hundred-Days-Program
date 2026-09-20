def main() -> None:
    from app.core.database import get_db
    db_generator = get_db()
    db = next(db_generator)
    print("Database session created successfully!")
    db.close()
    print("Database session closed successfully!")


if __name__ == "__main__":
    main()
