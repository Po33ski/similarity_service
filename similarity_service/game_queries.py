from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from models import Games
from database import get_engine
from embeddings import generate_embedding
from tqdm import tqdm

engine = get_engine()

def insert_games(dataset):
    """Insert games with progress bar"""
    with tqdm(total=len(dataset)) as pbar:
        for game in dataset:
            # Skip incomplete records
            if not all(game.get(field) for field in ["Name", "Windows", "Linux", "Mac", "Price"]):
                continue
                
            embedding = generate_embedding(game["About the game"] or "")
            game_obj = Games(
                name=game["Name"],
                description=(game["About the game"] or "")[:4096],
                windows=game["Windows"],
                linux=game["Linux"],
                mac=game["Mac"],
                price=float(game["Price"]),
                game_description_embedding=embedding
            )
            
            with Session(engine) as session:
                session.add(game_obj)
                session.commit()
            pbar.update(1)

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