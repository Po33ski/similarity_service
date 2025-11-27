from datasets import load_dataset
from game_queries import insert_games, find_similar_games

# This function sets up the database
def setup_database():
    dataset = load_dataset("FronkonGames/steam-games-dataset")
    dataset = dataset["train"].select(range(1000))  # Limit to 1k games
    insert_games(dataset)

# This function tests the search functionality
def test_search():
    print("\nCheap RPG games:")
    for game in find_similar_games(
        "epic fantasy RPG with dragons and magic",
        max_price=10.0,
        limit=3
    ):
        print(f"{game.name} (${game.price:.2f})")
    
    print("\nLinux strategy games:")
    for game in find_similar_games(
        "real-time strategy game",
        linux=True,
        min_score=0.4,
        limit=3
    ):
        print(f"{game.name} (Linux: {game.linux})")

if __name__ == "__main__":
    setup_database()
    test_search()