from queries import batch_insert_images, get_first_image, find_similar_images

def test_similarity_search():
    # Insert test data (100 images)
    batch_insert_images(100)
    
    # Get reference image
    reference = get_first_image()
    print(f"Reference image: {reference.image_path}")
    
    # Find similar images
    similar = find_similar_images(reference, k=5)
    
    print("\nMost similar images:")
    for img in similar:
        print(f"- {img.image_path} (ID: {img.id})")

if __name__ == "__main__":
    test_similarity_search()