import os
import sys
from pathlib import Path

# Get absolute paths
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = current_dir.parent
api_dir = project_root / 'API'

# Add API directory to system path
sys.path.append(str(api_dir))

from indexerAPI import IndexerAPI
from retrievalAPI import RetrievalAPI

def main():
    # Initialize systems
    try:
        indexer = IndexerAPI()
        retriever = RetrievalAPI()
        
        # Verify directories exist
        os.makedirs(indexer.NOTES_DIRECTORY, exist_ok=True)
        os.makedirs(indexer.EMBEDDINGS_DIRECTORY, exist_ok=True)
        
        print(f"Using directories:")
        print(f"Notes: {indexer.NOTES_DIRECTORY}")
        print(f"Embeddings: {indexer.EMBEDDINGS_DIRECTORY}")
        
        # Basic test notes
        basic_notes = [
            ("basic_note_1", "I went to college today"),
            ("basic_note_2", "నేను కాలేజీకి వెళ్లాను"),
            ("basic_note_3", "college lo classes unnai"),
            ("basic_note_4", "homework complete చేశాను")
        ]
        
        # Complex test notes
        complex_notes = [
            ("daily_log_1", """Today morning nenu office ki late ga vella..."""),
            ("study_notes", """Machine Learning concepts revision chesanu today..."""),
            ("recipe_note", """Amma's Special Biryani Recipe..."""),
            ("movie_review", """New movie చూశాను yesterday..."""),
            ("tech_notes", """Software Development meeting notes..."""),
            ("travel_diary", """Hyderabad trip experience...""")
        ]
        
        # Combine all test notes
        all_test_notes = basic_notes + complex_notes
        
        # Create and index notes
        print("\nCreating and indexing notes...")
        for note_id, content in all_test_notes:
            try:
                indexer.createNote(note_id)
                indexer.editNote(note_id, content)
                print(f"Successfully indexed note: {note_id}")
                
                # Verify embeddings
                bert_path = os.path.join(indexer.EMBEDDINGS_DIRECTORY, f"{note_id}_bert.npy")
                en_path = os.path.join(indexer.VEC_EN_DIR, f"{note_id}_ri.npy")
                te_path = os.path.join(indexer.VEC_TE_DIR, f"{note_id}_ri.npy")
                
                if all(os.path.exists(p) for p in [bert_path, en_path, te_path]):
                    bert_emb = np.load(bert_path)
                    en_emb = np.load(en_path)
                    te_emb = np.load(te_path)
                    print(f"Embeddings verified for {note_id}:")
                    print(f"BERT shape: {bert_emb.shape}")
                    print(f"English RI shape: {en_emb.shape}")
                    print(f"Telugu RI shape: {te_emb.shape}")
                else:
                    print(f"Warning: Some embeddings missing for {note_id}")
                    
            except Exception as e:
                print(f"Error indexing {note_id}: {str(e)}")
        
        # Combine all test queries
        all_test_queries = [
            # Basic queries
            "college",
            "కాలేజీ",
            "classes unnai",
            "homework చేశాను",
            
            # Work-related queries
            "office",
            "meeting",
            
            # Technical queries
            "machine",
            "software",
            
            # Recipe-related queries
            "biryani",
            "cooking",
            
            # Entertainment queries
            "movie",
            "entertainment related విషయాలు",
            
            # Travel-related queries
            "Hyderabad tourist places",
            "street food experiences చెప్పు",
            
            # Mixed context queries
            "food related అన్ని notes చూపించు",
            "timeline and planning related విషయాలు",
            
            # Complex queries
            "project work and learning concepts గురించి చెప్పు",
            "travel and food experiences నుండి information తీసుకురా"
        ]
        
        # Test retrieval
        print("\nTesting queries...")
        for query in all_test_queries:
            print(f"\nQuery: {query}")
            print("-" * 80)
            
            try:
                results = retriever.find(query)
                
                if not results:
                    print("No matching results found.")
                    processed_query = retriever._process_query(query)
                    print(f"Debug: Processed query: {processed_query}")
                    continue
                
                # Display results
                for idx, result in enumerate(results, 1):
                    print(f"\nResult {idx}:")
                    print(f"Note ID: {result['note_id']}")
                    print(f"Similarity Score: {result['similarity']:.4f}")
                    print("Content:")
                    print(result['content'].strip())
                    print("-" * 80)
                
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
                import traceback
                print(traceback.format_exc())
            
            print()
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        print(traceback.format_exc())
if __name__ == "__main__":
    main()