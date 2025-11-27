from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np
from models import Images
from database import get_engine

engine = get_engine()

#this function inserts a single image with its embedding into the database. TYhe image path is the path to the image and the image embedding is the embedding of the image.
#The image does not exist in the database. Its just a placeholder for the image and it is created only for the purpose of the test.
def insert_image(image_path: str, image_embedding: list[float]):
    """Insert a single image with its embedding"""
    with Session(engine) as session:
        image = Images(
            image_path=image_path,
            image_embedding=image_embedding
        )
        session.add(image)
        session.commit()
        return image

#this function inserts multiple images with random embeddings
def batch_insert_images(num_images: int):
    """Insert multiple test images with random embeddings"""
    for i in range(num_images):
        image_path = f"image_{i}.jpg"
        image_embedding = np.random.rand(512).tolist()  # 512-dim random vector
        insert_image(image_path, image_embedding)

def get_first_image():
    """Retrieve the first image from database"""
    with Session(engine) as session:
        return session.query(Images).first()

#this function finds the most similar images to the reference image
def find_similar_images(reference_image: Images, k: int = 10) -> list[Images]:
    """
    Find k most similar images using cosine similarity
    Returns list of Images objects ordered by similarity
    """
    with Session(engine) as session:
        result = session.execute(
            select(Images)
            .order_by(Images.image_embedding.cosine_distance(reference_image.image_embedding)) #here it compares
            .limit(k)
        )
        return result.scalars().all()