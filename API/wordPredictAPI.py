# wordPredictAPI.py
import numpy as np
import scipy.spatial as st
from time import gmtime, strftime
from ri import dsm, make_index, weight_func, remove_centroid, get_vec, get_index
import os
from pathlib import Path

class WordPredictAPI:
    def __init__(self, dimension=2000, window_size=4, nonzeros=8, delta=60):
        self.dimension = dimension
        self.window_size = window_size
        self.nonzeros = nonzeros
        self.delta = delta
        self.distvecs = None
        self.rivecs = None
        self.vocab = None
        
    def train(self, notes_directory):
        """Train the model using notes from directory"""
        # Collect all sentences from notes
        all_sentences = []
        
        # Read all .txt files from the notes directory
        for filename in os.listdir(notes_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(notes_directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        # Split text into sentences (you might want to improve this splitting)
                        sentences = [s.strip() for s in text.split('.') if s.strip()]
                        all_sentences.extend(sentences)
                except Exception as e:
                    print(f"Error reading file {filename}: {str(e)}")
        
        if not all_sentences:
            raise ValueError("No training data found in notes directory")
            
        # Write sentences to temporary file for dsm function
        with open("temp_training.txt", "w", encoding='utf-8') as f:
            for sentence in all_sentences:
                f.write(f"{sentence.strip()}\n")
        
        # Use dsm function for Random Indexing
        self.distvecs, self.rivecs, self.vocab = dsm(
            infile="temp_training.txt",
            win=self.window_size,
            trainfunc='direction',
            indexfunc='legacy',
            dimen=self.dimension,
            nonzeros=self.nonzeros,
            delta=self.delta,
            use_weights=True
        )
        
        # Remove centroid
        remove_centroid(self.distvecs)
        
        # Clean up temporary file
        try:
            os.remove("temp_training.txt")
        except:
            pass
    
    def predict_next_word(self, context, top_k=5):
        """Predict next words based on context"""
        if not self.vocab or not self.distvecs:
            return []
            
        context_words = context.strip().split()
        if not context_words:
            return []
        
        # Get context embedding
        context_vec = np.zeros(self.dimension)
        for word in context_words[-self.window_size:]:
            if word in self.vocab:
                word_vec = get_vec(word, self.vocab, self.distvecs)
                if word_vec is not False:
                    context_vec = np.add(context_vec, word_vec)
        
        # Ensure context_vec is 1-D
        context_vec = np.ravel(context_vec)
        
        # Calculate similarities
        similarities = []
        for word, (idx, freq) in self.vocab.items():
            if word not in context_words[-1:]:
                word_vec = get_vec(word, self.vocab, self.distvecs)
                if word_vec is not False:
                    word_vec = np.ravel(word_vec)
                    sim = 1 - st.distance.cosine(context_vec, word_vec)
                    if not np.isnan(sim):
                        weight = weight_func(freq, len(self.vocab), self.delta)
                        similarities.append((word, sim * weight))
        
        # Sort by weighted similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]