#!/usr/bin/env python3
"""
Main script for RAG (Retrieval-Augmented Generation) system with interactive menu.
This script provides an intelligent interface that detects existing embeddings
and offers appropriate options.
"""

import os
from milvus_rag_interface import MilvusRAGInterface


# Configuration
PDF_URL = "https://www.iab.org.pl/wp-content/uploads/2024/04/Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
FILE_NAME = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
FILE_JSON = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
EMBEDDINGS_JSON = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska-Embeddings.json"
COLLECTION_NAME = "rag_texts_and_embeddings"
DATA_DIR = "./milvus_db/data"


def check_embeddings_exist():
    """
    Check if both embeddings and text JSON files exist.
    
    Returns:
        bool: True if both files exist, False otherwise
    """
    embeddings_path = os.path.join(DATA_DIR, EMBEDDINGS_JSON)
    json_path = os.path.join(DATA_DIR, FILE_JSON)
    
    return os.path.exists(embeddings_path) and os.path.exists(json_path)


def check_pdf_exists():
    """
    Check if PDF file exists locally.
    
    Returns:
        bool: True if PDF exists, False otherwise
    """
    pdf_path = os.path.join(DATA_DIR, FILE_NAME)
    return os.path.exists(pdf_path)


def delete_old_files():
    """
    Delete old PDF, JSON, and embeddings files.
    """
    files_to_delete = [FILE_NAME, FILE_JSON, EMBEDDINGS_JSON]
    
    print("\n🗑️  Deleting old files...")
    for filename in files_to_delete:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"   Deleted: {filename}")
    print("✅ Old files deleted")


def process_new_embeddings(rag_interface, download_pdf=True):
    """
    Process document: download PDF (if needed), extract text, generate embeddings.
    
    Args:
        rag_interface: MilvusRAGInterface instance
        download_pdf: Whether to download PDF (True) or use existing one (False)
    """
    print("\n" + "=" * 80)
    print("Processing Document")
    print("=" * 80)
    
    # Download PDF if needed
    if download_pdf:
        print("\n📥 Downloading PDF...")
        rag_interface.download_pdf(PDF_URL, FILE_NAME)
    else:
        print(f"\n📄 Using existing PDF: {FILE_NAME}")
    
    # Extract text
    print("\n📝 Extracting text from PDF...")
    rag_interface.extract_pdf_text(FILE_NAME, FILE_JSON)
    
    # Generate embeddings
    print("\n🧠 Generating embeddings (this may take a few minutes)...")
    rag_interface.generate_embeddings(FILE_JSON, EMBEDDINGS_JSON)
    
    # Insert into database
    print("\n💾 Inserting embeddings into database...")
    rag_interface.insert_embeddings(FILE_JSON, EMBEDDINGS_JSON, COLLECTION_NAME)
    
    print("\n✅ Document processing complete!")


def interactive_chat(rag_interface):
    """
    Run interactive chat loop - only RAG queries, no file operations.
    
    Args:
        rag_interface: MilvusRAGInterface instance
    """
    print("\n" + "=" * 80)
    print("💬 Interactive Chat Mode")
    print("=" * 80)
    print("\nType your questions and get AI-powered answers based on the document.")
    print("Commands:")
    print("  • Type your question in English or Polish")
    print("  • 'quit' or 'exit' or 'q' - Exit chat")
    print("=" * 80 + "\n")
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if not question:
                print("⚠️  Please enter a question.\n")
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Exiting chat. Goodbye!")
                break
            
            print("\n🤔 Searching for relevant information...")
            
            # Determine language based on question (simple heuristic)
            # You can make this more sophisticated if needed
            language = "en"  # default to English
            
            response = rag_interface.rag(question, collection_name=COLLECTION_NAME, language=language)
            
            if response:
                print(f"\n💡 Answer:\n{response}\n")
            else:
                print("\n⚠️  No response generated. Check your API key.\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Exiting chat. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def show_menu():
    """
    Display the main menu for users when embeddings already exist.
    
    Returns:
        str: User's choice
    """
    print("\n" + "=" * 80)
    print("📋 MENU - Embeddings already exist")
    print("=" * 80)
    print("\n[1] 🔄 Delete old embeddings and create new ones")
    print("[2] 💬 Start chat (use existing embeddings)")
    print("[0] 🚪 Exit")
    print("\n" + "=" * 80)
    
    choice = input("\nSelect option [0-2]: ").strip()
    return choice


def main():
    """
    Main function with intelligent menu system.
    """
    print("=" * 80)
    print("🤖 RAG System - Retrieval-Augmented Generation with Milvus and Gemini")
    print("=" * 80)
    
    # Check if GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  WARNING: GOOGLE_API_KEY environment variable not set!")
        print("Please run: source env_setup.sh")
        print("Or set it manually: export GOOGLE_API_KEY='your_api_key_here'\n")
        return
    
    # Initialize RAG interface
    print("\n🔧 Initializing RAG Interface...")
    rag_interface = MilvusRAGInterface(
        host="./milvus_db/milvus_lite.db",
        port=None,
        embedding_model_name="ipipan/silver-retriever-base-v1.1"
    )
    
    # Create collection if it doesn't exist
    if not rag_interface.milvus_client.has_collection(COLLECTION_NAME):
        print(f"\n📦 Creating collection: {COLLECTION_NAME}")
        rag_interface.create_collection(
            collection_name=COLLECTION_NAME,
            schema_description="RAG Texts collection for AI guide"
        )
    else:
        print(f"\n✅ Collection '{COLLECTION_NAME}' already exists")
    
    # Check if embeddings exist
    embeddings_exist = check_embeddings_exist()
    
    if not embeddings_exist:
        # SCENARIO A: No embeddings - auto-process and start chat
        print("\n" + "=" * 80)
        print("🆕 First Time Setup Detected")
        print("=" * 80)
        print("\nNo embeddings found. Starting automatic document processing...")
        
        # Always download PDF on first run
        process_new_embeddings(rag_interface, download_pdf=True)
        
        # Automatically start chat
        interactive_chat(rag_interface)
        
    else:
        # SCENARIO B: Embeddings exist - show menu
        print("\n" + "=" * 80)
        print("✅ Embeddings Found")
        print("=" * 80)
        
        entry_count = rag_interface.count_entries(COLLECTION_NAME)
        print(f"\nDatabase contains {entry_count} entries")
        
        while True:
            choice = show_menu()
            
            if choice == '1':
                # Delete and recreate embeddings
                print("\n🔄 Recreating embeddings...")
                
                # Clear Milvus collection
                rag_interface.clear_collection(COLLECTION_NAME)
                
                # Delete old files
                delete_old_files()
                
                # Check if PDF exists, download if not
                pdf_exists = check_pdf_exists()
                process_new_embeddings(rag_interface, download_pdf=not pdf_exists)
                
                # Start chat after processing
                interactive_chat(rag_interface)
                break
                
            elif choice == '2':
                # Just start chat
                interactive_chat(rag_interface)
                break
                
            elif choice == '0':
                print("\n👋 Exiting. Goodbye!")
                break
                
            else:
                print("\n❌ Invalid option. Please select 0, 1, or 2.")
    
    print("\n" + "=" * 80)
    print("✅ RAG System session ended")
    print("=" * 80)


if __name__ == "__main__":
    main()
