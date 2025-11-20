import statistics
import random
import sys
import matplotlib.pyplot as plt
from fuzzywuzzy import process
from movie_storage import movie_storage_sql as db




def main():

    """Starts the movie database."""
    menu_actions = {
        "0": sys.exit,
        "1": list_movies,
        "2": add_movie,
        "3": delete_movie,
        "4": update_movie,
        "5": show_stats,
        "6": random_movie,
        "7": search_movie,
        "8": sort_movies_by_rating,
        "9": create_rating_histogram,
    }

    print("""
    ********** My Movies Database **********

    0. Exit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Create Rating Histogram
    """)

    while True:
        choice = input("Enter choice (0–9): ").strip()
        action = menu_actions.get(choice)
        if action:
            movies = db.get_movies()
            action(movies)
        else:
            print("Invalid choice. Please try again.")


def list_movies(movies):
    """Displays all movies with year and rating."""
    print(f"\n{len(movies)} movies in total:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): rating {data['rating']}")


def add_movie(movies):
    """Adds a new movie."""
    title = input("Enter movie name: ").strip()
    year = input("Enter release year: ").strip()
    rating = float(input("Enter rating (0–10): "))
    if db.add_movie(title, year, rating):

        print(f"Movie '{title}' added!")
    else:
        print("Movie could not be added. Movie already exists.")


def delete_movie(movies):
    """Deletes a movie."""
    title = input("Enter movie name to delete: ").strip()
    if title in movies:
        db.delete_movie(title)
        print(f"Movie '{title}' deleted!")
    else:
        print(f"Movie '{title}' not found!")


def update_movie(movies):
    """Updates a movie’s year and rating."""
    title = input("Enter movie name to update: ").strip()
    if title not in movies:
        print("Movie not found!")
        return
    year = input("Enter new year: ").strip()
    rating = float(input("Enter new rating (0–10): "))
    db.update_movie(title, year, rating)
    print(f"Movie '{title}' updated!")


def show_stats(movies):
    """Displays statistics about movie ratings."""
    ratings = [data["rating"] for data in movies.values()]
    if not ratings:
        print("No movies in database.")
        return

    avg = statistics.mean(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)

    best = [t for t, d in movies.items() if d["rating"] == max_rating]
    worst = [t for t, d in movies.items() if d["rating"] == min_rating]

    print(f"""
 Movie Statistics:
- Average rating: {avg:.2f}
- Median rating: {med}
- Best movies: {', '.join(best)}
- Worst movies: {', '.join(worst)}
""")


def random_movie(movies):
    """Selects a random movie."""
    if not movies:
        print("No movies available.")
        return
    title = random.choice(list(movies.keys()))
    data = movies[title]
    print(f"Random pick: {title} ({data['year']}) — Rating {data['rating']}")


def search_movie(movies):
    """Searches for movies by title or substring."""
    query = input("Enter part of the movie name: ").lower()
    matches = {t: d for t, d in movies.items() if query in t.lower()}

    if matches:
        for title, data in matches.items():
            print(f"{title} ({data['year']}): rating {data['rating']}")
    else:
        suggestions = process.extract(query, movies.keys(), limit=3)
        print("Did you mean:")
        for match, score in suggestions:
            print(f"  - {match} ({movies[match]['year']}) — {movies[match]['rating']}")


def sort_movies_by_rating(movies):
    """Sorts movies by rating (descending)."""
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def create_rating_histogram(movies):
    """Creates a histogram of movie ratings."""
    if not movies:
        print("No movies available.")
        return

    filename = input("Enter filename (without .png): ").strip()
    ratings = [data["rating"] for data in movies.values()]

    plt.hist(ratings, bins=10, edgecolor="black", range=(0, 10))
    plt.xlabel("Ratings")
    plt.ylabel("Number of Movies")
    plt.title("Histogram of Movie Ratings")
    plt.savefig(filename + ".png")
    plt.close()
    print(f"Histogram saved as {filename}.png")


if __name__ == "__main__":
    main()
