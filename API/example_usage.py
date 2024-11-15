from indexerAPI import IndexerAPI
from retrievalAPI import RetrievalAPI

def main():
    # Initialize systems
    indexer = IndexerAPI()
    retriever = RetrievalAPI()
    
    # Test notes with longer, more realistic code-mixed content
    test_notes = [
        ("daily_log_1", """
        Today morning nenu office ki late ga vella. Traffic chaala heavy ga undi. 
        Meeting lo project progress discuss chesamu. Client requirements change chesaru, 
        so timeline ni adjust cheyali. Lunch break lo new cafe ki vella, food bagundi. 
        Evening work complete chesi 7 PM ki intiki vacha."""),
        
        ("study_notes", """
        Machine Learning concepts revision chesanu today:
        1. Neural Networks basics అర్థం చేసుకున్నాను
        2. Backpropagation algorithm implementation చేశాను
        3. Gradient descent calculations practice చేశాను
        Next week exam ki preparation start చేయాలి."""),
        
        ("recipe_note", """
        Amma's Special Biryani Recipe:
        - Basmati rice ni 30 mins soak చేయాలి
        - Onions ni golden brown color వచ్చే వరకు fry చేయాలి
        - Chicken ni marinate చేసి 2 hours పెట్టాలి
        - Spices అన్నీ correct proportions లో వేయాలి
        - Dum process ki 20 mins పడుతుంది
        Final ga garnishing తో serve చేయాలి."""),
        
        ("movie_review", """
        New movie చూశాను yesterday. Cinematography చాలా బాగుంది, 
        కానీ story కొంచెం weak గా అనిపించింది. First half entertaining గా ఉంది,
        but second half లో bore కొట్టింది. Main lead acting impressive గా ఉంది,
        supporting cast performance కూడా బాగుంది. Overall ga one time watch movie."""),
        
        ("tech_notes", """
        Software Development meeting notes:
        - New features implement చేయడానికి timeline set చేశాము
        - Bug fixes priority list create చేశాము
        - Testing team తో coordination improve చేయాలి
        - Code optimization చేయాలి next sprint లో
        - Documentation update చేయడం pending లో ఉంది
        Next week release ki prepare అవుతున్నాము."""),
        
        ("travel_diary", """
        Hyderabad trip experience:
        Charminar దగ్గర street food try చేశాను, especially biryani amazing గా ఉంది.
        Golconda Fort history చాలా interesting గా ఉంది. Evening Hussain Sagar వద్ద 
        boat ride తీసుకున్నాము. Shopping కి Laad Bazaar వెళ్ళాము, traditional bangles 
        కొన్నాము. Local people చాలా friendly గా ఉన్నారు.""")
    ]
    
    # Create and index notes
    print("Creating and indexing notes...")
    for note_id, content in test_notes:
        try:
            indexer.createNote(note_id)
            indexer.editNote(note_id, content)
            print(f"Indexed note: {note_id}")
        except Exception as e:
            print(f"Error indexing {note_id}: {str(e)}")
    
    # Test queries with various scenarios
    test_queries = [
        # Work-related queries
        "office work progress ఎలా ఉంది?",
        "meeting notes చూపించు",
        
        # Technical queries
        "machine learning concepts explain చేయి",
        "software development timeline ఏంటి?",
        
        # Recipe-related queries
        "biryani recipe ఎలా చేయాలి?",
        "cooking instructions చెప్పు",
        
        # Entertainment queries
        "movie review ఎలా ఉంది?",
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
    
    # Search notes
    print("\nTesting queries...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        results = retriever.find(query)
        
        if not results:
            print("No matching results found.")
            continue
            
        for idx, result in enumerate(results, 1):
            print(f"\nResult {idx}:")
            print(f"Note ID: {result['note_id']}")
            print(f"Similarity Score: {result['similarity']:.4f}")
            print("\nContent:")
            print(result['content'].strip())
            print("-" * 80)
        print("\n")

if __name__ == "__main__":
    main()