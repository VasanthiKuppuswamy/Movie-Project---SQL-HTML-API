from sqlalchemy import create_engine, text

# SQLite database connection
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=True)

# Create table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


def get_movies():
    """Return all movies as a dictionary (compatible with movies.py)."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                {"title": title, "year": year, "rating": rating},
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title},
        )
        connection.commit()
        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, year, rating):
    """Update a movie’s year and rating in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                UPDATE movies
                SET year = :year, rating = :rating
                WHERE title = :title
            """),
            {"title": title, "year": year, "rating": rating},
        )
        connection.commit()
        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")
