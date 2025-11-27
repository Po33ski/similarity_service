#!/usr/bin/env python3
"""
Demo script for similarity search in games database.
Shows how to search for similar games with various filters.
"""

from game_queries import find_similar_games
from sqlalchemy.orm import Session
from database import get_engine
from models import Games

# This function counts the total games in the database
def count_games():
    """Count total games in database"""
    engine = get_engine()
    with Session(engine) as session:
        return session.query(Games).count()


# This function demonstrates various similarity search queries
def demo_search():
    """
    Demonstrate various similarity search queries.
    """
    print("=" * 80)
    print("🎮 Game Similarity Search Demo")
    print("=" * 80)
    
    # Check if database has data
    total_games = count_games()
    print(f"\n📊 Database contains {total_games} games")
    
    if total_games == 0:
        print("\n⚠️  No games in database!")
        print("Please run: python tests/test_games.py")
        print("This will load 40,000 games from Steam dataset (takes ~30 minutes)")
        return
    
    print("\n" + "=" * 80)
    
    # Query 1: Cheap RPG games
    print("\n🔍 Query 1: Looking for cheap fantasy RPG games...")
    print("Description: 'epic fantasy RPG with dragons and magic'")
    print("Filters: max_price=$10, limit=5\n")
    
    games = find_similar_games(
        "epic fantasy RPG with dragons and magic",
        max_price=10.0,
        limit=5
    )
    
    for i, game in enumerate(games, 1):
        print(f"{i}. {game.name}")
        print(f"   Price: ${game.price:.2f}")
        print(f"   Platforms: {'Win' if game.windows else ''} "
              f"{'Linux' if game.linux else ''} {'Mac' if game.mac else ''}")
        print(f"   Description: {game.description[:100]}...")
        print()
    
    # Query 2: Linux strategy games
    print("=" * 80)
    print("\n🔍 Query 2: Looking for strategy games on Linux...")
    print("Description: 'real-time strategy game with base building'")
    print("Filters: linux=True, min_score=0.4, limit=5\n")
    
    games = find_similar_games(
        "real-time strategy game with base building",
        linux=True,
        min_score=0.4,
        limit=5
    )
    
    for i, game in enumerate(games, 1):
        print(f"{i}. {game.name}")
        print(f"   Price: ${game.price:.2f}")
        print(f"   Linux: ✅")
        print(f"   Description: {game.description[:100]}...")
        print()
    
    # Query 3: Multiplayer action games
    print("=" * 80)
    print("\n🔍 Query 3: Looking for multiplayer action games...")
    print("Description: 'fast-paced multiplayer shooter with competitive gameplay'")
    print("Filters: max_price=$30, limit=5\n")
    
    games = find_similar_games(
        "fast-paced multiplayer shooter with competitive gameplay",
        max_price=30.0,
        limit=5
    )
    
    for i, game in enumerate(games, 1):
        print(f"{i}. {game.name}")
        print(f"   Price: ${game.price:.2f}")
        print(f"   Description: {game.description[:100]}...")
        print()
    
    # Query 4: Free puzzle games
    print("=" * 80)
    print("\n🔍 Query 4: Looking for free puzzle games...")
    print("Description: 'relaxing puzzle game with colorful graphics'")
    print("Filters: max_price=$0, limit=5\n")
    
    games = find_similar_games(
        "relaxing puzzle game with colorful graphics",
        max_price=0.0,
        limit=5
    )
    
    for i, game in enumerate(games, 1):
        print(f"{i}. {game.name}")
        print(f"   Price: FREE")
        print(f"   Description: {game.description[:100]}...")
        print()
    
    # Interactive mode
    print("=" * 80)
    print("\n💬 Interactive Search Mode")
    print("Type your game description to find similar games, or 'quit' to exit")
    print("=" * 80 + "\n")
    
    while True:
        try:
            description = input("\n🎮 Describe the game you're looking for: ").strip()
            
            if not description:
                print("⚠️  Please enter a description")
                continue
                
            if description.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Ask for optional filters
            max_price_input = input("Max price (press Enter for no limit): ").strip()
            max_price = float(max_price_input) if max_price_input else None
            
            platform = input("Platform (windows/linux/mac, or Enter for any): ").strip().lower()
            platform_filter = {}
            if platform == 'windows':
                platform_filter['windows'] = True
            elif platform == 'linux':
                platform_filter['linux'] = True
            elif platform == 'mac':
                platform_filter['mac'] = True
            
            print("\n🔍 Searching...")
            
            games = find_similar_games(
                description,
                max_price=max_price,
                limit=5,
                **platform_filter
            )
            
            if not games:
                print("❌ No games found matching your criteria")
                continue
            
            print(f"\n✅ Found {len(games)} similar games:\n")
            
            for i, game in enumerate(games, 1):
                print(f"{i}. {game.name}")
                print(f"   Price: ${game.price:.2f}")
                platforms = []
                if game.windows:
                    platforms.append("Windows")
                if game.linux:
                    platforms.append("Linux")
                if game.mac:
                    platforms.append("Mac")
                print(f"   Platforms: {', '.join(platforms)}")
                print(f"   Description: {game.description[:150]}...")
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    demo_search()

