from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from models import Games
from database import get_engine
from embeddings import generate_embedding
from tqdm import tqdm

engine = get_engine()

# This function inserts games into the database with a progress bar
def insert_games(dataset):
    """Insert games with progress bar"""
    with tqdm(total=len(dataset)) as pbar:
        for game in dataset:
            name = (game.get("Name") or "").strip()
            price = game.get("Price")

            # Skip entries missing essential information
            if not name or price is None:
                pbar.update(1)
                continue

            description = (game.get("About the game") or "")[:4096]
            windows = bool(game.get("Windows"))
            linux = bool(game.get("Linux"))
            mac = bool(game.get("Mac"))

            game_obj = Games(
                name=name,
                description=description,
                windows=windows,
                linux=linux,
                mac=mac,
                price=float(price),
                game_description_embedding=generate_embedding(description)
            )

            with Session(engine) as session:
                session.add(game_obj)
                session.commit()

            pbar.update(1)

# This function finds similar games with optional filters
def find_similar_games(
    description: str,
    min_score: Optional[float] = None,
    max_price: Optional[float] = None,
    windows: Optional[bool] = None,
    linux: Optional[bool] = None,
    mac: Optional[bool] = None,
    limit: int = 5
):
    """Find games with optional filters"""
    embedding = generate_embedding(description)
    
    with Session(engine) as session:
        query = (
            select(Games)
            .order_by(Games.game_description_embedding.cosine_distance(embedding))
        )
        
        # Apply filters
        if max_price is not None:
            query = query.filter(Games.price <= max_price)
        if windows is not None:
            query = query.filter(Games.windows == windows)
        if linux is not None:
            query = query.filter(Games.linux == linux)
        if mac is not None:
            query = query.filter(Games.mac == mac)
            
        if min_score is not None:
            # Convert cosine distance to similarity (1 - distance)
            query = query.filter(
                1 - Games.game_description_embedding.cosine_distance(embedding) > min_score
            )
            
        result = session.execute(query.limit(limit))
        return result.scalars().all()