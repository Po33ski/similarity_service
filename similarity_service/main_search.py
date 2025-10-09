#!/usr/bin/env python3
"""
Main entry point for Similarity Search System.
Automatically starts database, checks data, and launches interactive search.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from game_queries import find_similar_games
from database import get_engine
from models import Games
from sqlalchemy.orm import Session


def check_docker_running():
    """Check if Docker is available"""
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def check_database_running():
    """Check if PostgreSQL container is running"""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=vectorscaledb', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return 'vectorscaledb' in result.stdout
    except:
        return False


def start_database():
    """Start PostgreSQL database using docker compose"""
    print("\n🚀 Starting PostgreSQL database...")
    
    project_root = Path(__file__).parent.parent
    vectorscale_dir = project_root / 'vectorscale_db'
    
    try:
        # Start docker compose
        result = subprocess.run(
            ['docker', 'compose', 'up', '-d'],
            cwd=str(vectorscale_dir),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to start database: {result.stderr}")
            return False
        
        print("✅ Database container started")
        
        # Wait for database to be ready
        print("⏳ Waiting for database to initialize (10 seconds)...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting database: {e}")
        return False


def count_games():
    """Count total games in database"""
    try:
        engine = get_engine()
        with Session(engine) as session:
            return session.query(Games).count()
    except Exception as e:
        print(f"⚠️  Could not count games: {e}")
        return 0


def load_sample_data():
    """Load 200 sample games"""
    print("\n📦 Loading sample data (200 games)...")
    print("This will take about 2-3 minutes...")
    
    try:
        # Import here to avoid circular imports
        from datasets import load_dataset
        from game_queries import insert_games
        
        print("\n🔄 Downloading Steam Games dataset...")
        dataset = load_dataset("FronkonGames/steam-games-dataset")
        
        print("📊 Selecting 200 games...")
        sample = dataset["train"].select(range(200))
        
        print("\n💾 Generating embeddings and inserting into database...")
        print("(Each game description is converted to a 512-dim vector)")
        insert_games(sample)
        
        print("\n✅ Sample data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to load data: {e}")
        return False


def interactive_search():
    """Run interactive game search"""
    print("\n" + "=" * 80)
    print("🔍 GAME SEARCH - Interactive Mode")
    print("=" * 80)
    print("\n💡 Tips:")
    print("   • Describe the game you're looking for (e.g., 'fantasy RPG')")
    print("   • Set optional filters: max price, platform")
    print("   • Type 'quit' or 'exit' to stop")
    print("\n📚 Example queries:")
    print("   • 'space exploration game'")
    print("   • 'horror survival'")
    print("   • 'strategy with base building'")
    print("   • 'indie platformer'")
    print("   • 'multiplayer shooter'")
    print("\n" + "=" * 80 + "\n")
    
    while True:
        try:
            # Get search query
            query = input("🎮 What game are you looking for? ").strip()
            
            if not query:
                print("⚠️  Please enter a description.\n")
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Get optional filters
            try:
                max_price_input = input("💰 Max price (Enter for any): ").strip()
                max_price = float(max_price_input) if max_price_input else None
            except:
                print("⚠️  Invalid price, ignoring filter")
                max_price = None
            
            platform = input("💻 Platform (windows/linux/mac or Enter for any): ").strip().lower()
            filters = {}
            
            if platform in ['windows', 'win', 'w']:
                filters['windows'] = True
                print("   🪟 Filtering: Windows only")
            elif platform in ['linux', 'l']:
                filters['linux'] = True
                print("   🐧 Filtering: Linux only")
            elif platform in ['mac', 'm']:
                filters['mac'] = True
                print("   🍎 Filtering: Mac only")
            
            # Search
            print("\n🔍 Searching for similar games...\n")
            
            games = find_similar_games(
                query,
                max_price=max_price,
                limit=5,
                **filters
            )
            
            if not games:
                print("❌ No games found matching your criteria.")
                print("💡 Try:")
                print("   • Different search terms")
                print("   • Removing filters")
                print("   • Loading more data\n")
                continue
            
            print(f"✅ Found {len(games)} similar games:\n")
            
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
                
                desc = game.description[:120] + "..." if len(game.description) > 120 else game.description
                print(f"   📝 {desc}")
                print()
            
            print("─" * 80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def show_menu(game_count):
    """Show menu when games exist"""
    print("\n" + "=" * 80)
    print(f"📊 Database Status: {game_count} games available")
    print("=" * 80)
    print("\n[1] 🔍 Start game search")
    print("[2] 📦 Load more games (200 additional)")
    print("[0] 🚪 Exit")
    print("\n" + "=" * 80)
    
    choice = input("\nSelect option [0-2]: ").strip()
    return choice


def main():
    """Main function - orchestrates the entire flow"""
    print("=" * 80)
    print("🎮 SIMILARITY SEARCH SYSTEM")
    print("   Semantic Game Search using PostgreSQL + pgvectorscale")
    print("=" * 80)
    
    # Step 1: Check Docker
    print("\n🔍 Step 1: Checking Docker...")
    if not check_docker_running():
        print("❌ Docker is not running or not available!")
        print("\n💡 Solutions:")
        print("   1. Start Docker Desktop")
        print("   2. Enable WSL2 integration in Docker Desktop settings")
        print("   3. Restart your terminal")
        sys.exit(1)
    print("✅ Docker is available")
    
    # Step 2: Check/Start Database
    print("\n🔍 Step 2: Checking database...")
    if not check_database_running():
        print("⚠️  Database not running")
        
        response = input("\n❓ Start database now? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("❌ Database required. Exiting.")
            sys.exit(1)
        
        if not start_database():
            print("\n❌ Failed to start database. Please check Docker and try again.")
            sys.exit(1)
    else:
        print("✅ Database is running")
    
    # Step 3: Check data
    print("\n🔍 Step 3: Checking data...")
    game_count = count_games()
    
    if game_count == 0:
        print("⚠️  No games in database")
        print("\n" + "=" * 80)
        print("🆕 FIRST TIME SETUP")
        print("=" * 80)
        print("\nTo use the search system, we need to load some games first.")
        print("This will download 200 games from Steam and generate embeddings.")
        print("\n⏱️  Estimated time: 2-3 minutes")
        
        response = input("\n❓ Load sample data now? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            if load_sample_data():
                game_count = count_games()
                print(f"\n✅ Database now contains {game_count} games")
                print("\n🚀 Starting search interface...\n")
                time.sleep(2)
                interactive_search()
            else:
                print("\n❌ Failed to load data. Please try again later.")
                sys.exit(1)
        else:
            print("\n💡 You can load data later by running:")
            print("   cd similarity_service")
            print("   uv run python quick_demo.py")
            sys.exit(0)
    else:
        # Games exist - show menu
        while True:
            choice = show_menu(game_count)
            
            if choice == '1':
                # Start search
                interactive_search()
                break
                
            elif choice == '2':
                # Load more data
                if load_sample_data():
                    game_count = count_games()
                    print(f"\n✅ Database now contains {game_count} games")
                else:
                    print("\n❌ Failed to load data")
                # Return to menu
                
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
                
            else:
                print("\n❌ Invalid option. Please select 0, 1, or 2.")
    
    print("\n" + "=" * 80)
    print("✅ Similarity Search System session ended")
    print("=" * 80)
    print("\n💡 To stop the database:")
    print("   cd vectorscale_db && docker compose down\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

