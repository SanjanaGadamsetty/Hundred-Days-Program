def main() -> None:
    from app.core.database import create_tables
    create_tables()
    print("Database tables created successfully!")


if __name__ == "__main__":
    main()
