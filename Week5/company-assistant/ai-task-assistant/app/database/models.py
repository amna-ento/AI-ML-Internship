from app.database.database import get_connection


def create_tables():
    connection = get_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    connection.commit()
    connection.close()


def seed_users():
    connection = get_connection()

    users = [
        ("Ahmed", "ahmed@example.com"),
        ("Ali", "ali@example.com")
    ]

    for name, email in users:
        connection.execute(
            "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )

    connection.commit()
    connection.close()