import os
import torch
import numpy as np
from dotenv import load_dotenv
from transformers import BertTokenizer, BertModel
from ri import dsm, make_index, weight_func, remove_centroid
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'inputProcesser'))
from TenglishFormatter import process_user_input

load_dotenv()

class IndexerAPI:
    def __init__(self, dimension=300, nonzeros=8, delta=60):
        """Initialize the indexer with both BERT and Random Indexing"""
        self.NOTES_DIRECTORY = os.getenv("NOTES_DIRECTORY")
        self.EMBEDDINGS_DIRECTORY = os.getenv("EMBEDDINGS_DIRECTORY")
        
        
        self.VEC_EN_DIR = os.getenv("VEC_EN_DIR")
        self.VEC_TE_DIR = os.getenv("VEC_TE_DIR")
        
        for directory in [self.NOTES_DIRECTORY, self.EMBEDDINGS_DIRECTORY, self.VEC_EN_DIR, self.VEC_TE_DIR]:
            os.makedirs(directory, exist_ok=True)
        
        # BERT initialization
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Random Indexing parameters
        self.dimension = dimension
        self.nonzeros = nonzeros
        self.delta = delta
        self.en_vocab = {}
        self.te_vocab = {}
        self.en_vectors = []
        self.te_vectors = []
        self.bert_dimension = 768  # Add this line
        self.ri_dimension = dimension
        
        self._load_vocabularies()

    def createNote(self, fileName):
        """Create a new note file"""
        file_path = os.path.join(self.NOTES_DIRECTORY, f"{fileName}.txt")
        if os.path.exists(file_path):
            raise FileExistsError(f"The file '{fileName}.txt' already exists.")
        with open(file_path, 'w') as file:
            file.write("")
        print(f"File '{fileName}.txt' created at: {file_path}")

    def editNote(self, fileName, inputText):
        """Edit note and update embeddings"""
        file_path = os.path.join(self.NOTES_DIRECTORY, f"{fileName}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{fileName}.txt' does not exist.")
            
        processed_text = process_user_input(inputText)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)

        # Update embeddings
        self._update_embeddings(fileName, processed_text)

    def _update_embeddings(self, fileName, text):
        try:
            # BERT embedding
            bert_embedding = self._compute_bert_embedding(text)
            bert_path = os.path.join(self.EMBEDDINGS_DIRECTORY, f"{fileName}_bert.npy")
            np.save(bert_path, bert_embedding)
            print(f"Saved BERT embedding with shape: {bert_embedding.shape}")

            # Split languages
            en_words, te_words = self._split_languages(text)
            
            # Compute and save English RI embedding
            if en_words:
                en_embedding = self._compute_ri_embedding_for_language(en_words, self.en_vocab, self.en_vectors)
                en_path = os.path.join(self.VEC_EN_DIR, f"{fileName}_ri.npy")
                np.save(en_path, en_embedding)
                print(f"Saved English RI embedding with shape: {en_embedding.shape}")
            
            # Compute and save Telugu RI embedding
            if te_words:
                te_embedding = self._compute_ri_embedding_for_language(te_words, self.te_vocab, self.te_vectors)
                te_path = os.path.join(self.VEC_TE_DIR, f"{fileName}_ri.npy")
                np.save(te_path, te_embedding)
                print(f"Saved Telugu RI embedding with shape: {te_embedding.shape}")
            
            # Save vocabularies
            self._save_vocabularies()
            
        except Exception as e:
            print(f"Error updating embeddings: {str(e)}")
            raise
        
        
    def _compute_bert_embedding(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use pooler_output for consistent dimensionality
            embedding = outputs.pooler_output.cpu().numpy()
            
            # Handle NaN values
            embedding = np.nan_to_num(embedding, nan=0.0)
            
            # Normalize the embedding
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
                
            return embedding.reshape(1, self.bert_dimension)
        
    def _split_languages(self, text):
        """Split text into English and Telugu words"""
        words = text.split()
        en_words = [w.lower() for w in words if all(ord(c) < 128 for c in w)]
        te_words = [w for w in words if not all(ord(c) < 128 for c in w)]
        return en_words, te_words

    def _compute_ri_embedding(self, text):
        """Compute combined RI embedding for query processing"""
        if isinstance(text, str):
            words = text.split()
        else:
            words = text if isinstance(text, list) else []
            
        if not words:
            return np.zeros((1, self.ri_dimension))
        
        # Split into languages
        en_words = [w.lower() for w in words if all(ord(c) < 128 for c in w)]
        te_words = [w for w in words if not all(ord(c) < 128 for c in w)]
        
        # Compute embeddings for each language
        en_vector = np.zeros(self.ri_dimension)
        te_vector = np.zeros(self.ri_dimension)
        
        if en_words:
            en_vector = self._compute_ri_embedding_for_language(en_words, self.en_vocab, self.en_vectors)[0]
        if te_words:
            te_vector = self._compute_ri_embedding_for_language(te_words, self.te_vocab, self.te_vectors)[0]
        
        # Combine vectors
        combined_vector = en_vector + te_vector
        if np.any(combined_vector):
            combined_vector = combined_vector / np.linalg.norm(combined_vector)
        
        return combined_vector.reshape(1, self.ri_dimension)
    
    def _compute_ri_embedding_for_language(self, words, vocab, vectors):
        """Compute RI embedding for a specific language"""
        if not words:
            return np.zeros((1, self.ri_dimension))
        
        # Create document vector using Random Indexing
        doc_vector = make_index(self.dimension, self.nonzeros)
        word_count = 0
        
        # Create word vector
        word_vector = np.zeros(self.ri_dimension)
        
        for word in words:
            if word not in vocab:
                # Add new word to vocabulary
                vocab[word] = [len(vectors), 1]
                vectors.append(np.zeros(self.dimension))
            else:
                vocab[word][1] += 1
            
            # Update word vector
            idx = vocab[word][0]
            weight = weight_func(vocab[word][1], len(vocab), self.delta)
            np.add.at(vectors[idx], doc_vector[:,0], doc_vector[:,1] * weight)
            word_vector += vectors[idx]
            word_count += 1
        
        # Average and normalize
        if word_count > 0:
            word_vector = word_vector / word_count
            norm = np.linalg.norm(word_vector)
            if norm > 0:
                word_vector = word_vector / norm
        
        print(f"Created RI embedding from {word_count}/{len(words)} words")
        return word_vector.reshape(1, self.ri_dimension)
    
    def _save_vocabularies(self):
        """Save vocabularies and vectors"""
        # Save English vocabulary and vectors
        en_path = os.path.join(self.VEC_EN_DIR, "vocab.npz")
        np.savez(en_path,
                vocab=self.en_vocab,
                vectors=self.en_vectors)
        
        # Save Telugu vocabulary and vectors
        te_path = os.path.join(self.VEC_TE_DIR, "vocab.npz")
        np.savez(te_path,
                vocab=self.te_vocab,
                vectors=self.te_vectors)
        
    def _load_vocabularies(self):
        """Load existing vocabularies"""
        # Load English vocabulary and vectors
        en_path = os.path.join(self.VEC_EN_DIR, "vocab.npz")
        if os.path.exists(en_path):
            data = np.load(en_path, allow_pickle=True)
            self.en_vocab = data['vocab'].item()
            self.en_vectors = data['vectors']
        
        # Load Telugu vocabulary and vectors
        te_path = os.path.join(self.VEC_TE_DIR, "vocab.npz")
        if os.path.exists(te_path):
            data = np.load(te_path, allow_pickle=True)
            self.te_vocab = data['vocab'].item()
            self.te_vectors = data['vectors']