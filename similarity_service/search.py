#!/usr/bin/env python3
"""
Simple interactive search tool - just ask for games!
"""

from game_queries import find_similar_games

def search():
    print("=" * 80)
    print("🔍 Game Search - Type what you're looking for")
    print("=" * 80)
    print("\nExamples:")
    print("  - 'space exploration game'")
    print("  - 'horror survival'")
    print("  - 'strategy with base building'")
    print("\nType 'quit' to exit\n")
    print("=" * 80 + "\n")
    
    while True:
        # Get query
        query = input("🎮 What game are you looking for? ").strip()
        
        if not query:
            continue
            
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Get optional filters
        try:
            max_price = input("💰 Max price (Enter for any): ").strip()
            max_price = float(max_price) if max_price else None
        except:
            max_price = None
        
        platform = input("💻 Platform (windows/linux/mac or Enter for any): ").strip().lower()
        filters = {}
        if platform in ['windows', 'win', 'w']:
            filters['windows'] = True
        elif platform in ['linux', 'l']:
            filters['linux'] = True
        elif platform in ['mac', 'm']:
            filters['mac'] = True
        
        # Search
        print("\n🔍 Searching...\n")
        
        games = find_similar_games(
            query,
            max_price=max_price,
            limit=5,
            **filters
        )
        
        if not games:
            print("❌ No games found. Try different query or filters.\n")
            continue
        
        print(f"✅ Found {len(games)} games:\n")
        
        for i, game in enumerate(games, 1):
            print(f"{i}. 🎯 {game.name}")
            print(f"   💵 Price: ${game.price:.2f}")
            
            platforms = []
            if game.windows:
                platforms.append("🪟 Windows")
            if game.linux:
                platforms.append("🐧 Linux")
            if game.mac:
                platforms.append("🍎 Mac")
            if platforms:
                print(f"   📱 Platforms: {', '.join(platforms)}")
            
            desc = game.description[:150] + "..." if len(game.description) > 150 else game.description
            print(f"   📝 {desc}")
            print()
        
        print("=" * 80 + "\n")

if __name__ == "__main__":
    search()

