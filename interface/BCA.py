class BidirectionalAnalyzer:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.context_weights = {}
        
    def analyze_context(self, text):
        words = text.split()
        context_map = {}
        
        for i in range(len(words)):
            # Get left context
            left_start = max(0, i - self.window_size)
            left_context = words[left_start:i]
            
            # Get right context
            right_end = min(len(words), i + self.window_size + 1)
            right_context = words[i+1:right_end]
            
            # Store bidirectional context
            context_map[words[i]] = {
                'left': left_context,
                'right': right_context
            }
            
        return context_map


class SimpleAttention:
    def __init__(self):
        self.word_importance = {}
        
    def calculate_attention_scores(self, word, context):
        # Simple frequency-based attention
        score = 0
        for context_word in context:
            if (word, context_word) in self.word_importance:
                score += self.word_importance[(word, context_word)]
            else:
                score += 1  # Base attention score
                
        return score / len(context) if context else 0
        
    def update_importance(self, word, context_word, score):
        self.word_importance[(word, context_word)] = score


class ContextProcessor:
    def __init__(self):
        self.stop_words = set(['the', 'is', 'at', 'which', 'on'])
        self.punctuation = set(['.', ',', '!', '?', ';'])
        
    def clean_text(self, text):
        # Remove punctuation
        for punct in self.punctuation:
            text = text.replace(punct, ' ')
        
        # Convert to lowercase and split
        words = text.lower().split()
        
        # Remove stop words
        words = [w for w in words if w not in self.stop_words]
        
        return ' '.join(words)
        
    def extract_phrases(self, text, window_size=3):
        words = text.split()
        phrases = []
        
        for i in range(len(words) - window_size + 1):
            phrases.append(' '.join(words[i:i+window_size]))
            
        return phrases



class BidirectionalContextSystem:
    def __init__(self):
        self.analyzer = BidirectionalAnalyzer()
        self.attention = SimpleAttention()
        self.processor = ContextProcessor()
        
    def analyze_text(self, text):
        # Clean and process text
        cleaned_text = self.processor.clean_text(text)
        
        # Get bidirectional context
        context_map = self.analyzer.analyze_context(cleaned_text)
        
        # Calculate attention scores
        attention_scores = {}
        for word, contexts in context_map.items():
            left_score = self.attention.calculate_attention_scores(
                word, contexts['left'])
            right_score = self.attention.calculate_attention_scores(
                word, contexts['right'])
            attention_scores[word] = (left_score + right_score) / 2
            
        return {
            'context_map': context_map,
            'attention_scores': attention_scores
        }
        
    def get_key_phrases(self, text):
        analysis = self.analyze_text(text)
        scores = analysis['attention_scores']
        
        # Sort words by attention scores
        important_words = sorted(
            scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return [word for word, score in important_words]



def main():
    # Initialize the system
    context_system = BidirectionalContextSystem()
    
    # Example text
    text = """Natural language processing helps computers 
              understand and interpret human language. 
              This technology enables better communication 
              between humans and machines."""
    
    # Analyze text
    results = context_system.analyze_text(text)
    
    # Get key phrases
    key_phrases = context_system.get_key_phrases(text)
    
    print("Key phrases:", key_phrases)
    print("\nDetailed context analysis:")
    for word, contexts in results['context_map'].items():
        print(f"\nWord: {word}")
        print(f"Left context: {contexts['left']}")
        print(f"Right context: {contexts['right']}")
        print(f"Attention score: {results['attention_scores'][word]:.2f}")

if __name__ == "__main__":
    main()