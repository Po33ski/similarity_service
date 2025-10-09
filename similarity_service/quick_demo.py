#!/usr/bin/env python3
"""
Quick demo - loads small dataset and demonstrates search
"""

from datasets import load_dataset
from game_queries import insert_games, find_similar_games

def load_sample_data():
    """Load a small sample of games for demo"""
    print("=" * 80)
    print("📦 Loading sample data from Steam Games Dataset")
    print("=" * 80)
    
    print("\n🔄 Downloading dataset (this may take a minute)...")
    dataset = load_dataset("FronkonGames/steam-games-dataset")
    
    # Use only 200 games for quick demo
    print("📊 Selecting 200 games for demo...")
    sample = dataset["train"].select(range(200))
    
    print("\n💾 Inserting games into database...")
    print("(This generates embeddings for each game description)")
    insert_games(sample)
    
    print("\n✅ Sample data loaded successfully!")
    print(f"   {len(sample)} games are now in the database\n")


def run_demo_searches():
    """Run example searches"""
    print("=" * 80)
    print("🔍 Demo Searches")
    print("=" * 80)
    
    # Search 1: RPG games
    print("\n1️⃣  Looking for fantasy RPG games under $20...")
    print("   Query: 'fantasy RPG with magic and dragons'")
    print("   Filter: max_price=$20\n")
    
    games = find_similar_games(
        "fantasy RPG with magic and dragons",
        max_price=20.0,
        limit=3
    )
    
    if games:
        for i, game in enumerate(games, 1):
            print(f"   {i}. {game.name}")
            print(f"      Price: ${game.price:.2f}")
            print(f"      Description: {game.description[:80]}...\n")
    else:
        print("   No games found\n")
    
    # Search 2: Strategy games
    print("-" * 80)
    print("\n2️⃣  Looking for strategy games...")
    print("   Query: 'real-time strategy base building'")
    print("   Filter: limit=3\n")
    
    games = find_similar_games(
        "real-time strategy base building",
        limit=3
    )
    
    if games:
        for i, game in enumerate(games, 1):
            print(f"   {i}. {game.name}")
            print(f"      Price: ${game.price:.2f}")
            platforms = []
            if game.windows:
                platforms.append("Win")
            if game.linux:
                platforms.append("Linux")
            if game.mac:
                platforms.append("Mac")
            print(f"      Platforms: {' '.join(platforms)}")
            print(f"      Description: {game.description[:80]}...\n")
    else:
        print("   No games found\n")
    
    # Search 3: Puzzle games
    print("-" * 80)
    print("\n3️⃣  Looking for free puzzle games...")
    print("   Query: 'puzzle game with colorful graphics'")
    print("   Filter: max_price=$0 (free games only)\n")
    
    games = find_similar_games(
        "puzzle game with colorful graphics",
        max_price=0.0,
        limit=3
    )
    
    if games:
        for i, game in enumerate(games, 1):
            print(f"   {i}. {game.name}")
            print(f"      Price: FREE")
            print(f"      Description: {game.description[:80]}...\n")
    else:
        print("   No free puzzle games found in sample\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🎮 Similarity Search System - Quick Demo")
    print("=" * 80 + "\n")
    
    # Load sample data
    load_sample_data()
    
    # Run demo searches
    run_demo_searches()
    
    print("=" * 80)
    print("✅ Demo complete!")
    print("=" * 80)
    print("\n💡 To load more games: python tests/test_games.py")
    print("💡 For interactive search: python demo_search.py\n")

