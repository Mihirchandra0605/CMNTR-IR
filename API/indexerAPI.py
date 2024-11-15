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
        
        # Create directories if they don't exist
        os.makedirs(self.NOTES_DIRECTORY, exist_ok=True)
        os.makedirs(self.EMBEDDINGS_DIRECTORY, exist_ok=True)
        
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
        """Update both BERT and RI embeddings"""
        # BERT embedding
        bert_embedding = self._compute_bert_embedding(text)
        bert_path = os.path.join(self.EMBEDDINGS_DIRECTORY, f"{fileName}_bert.npy")
        np.save(bert_path, bert_embedding)

        # Random Indexing
        en_words, te_words = self._split_languages(text)
        ri_embedding = self._compute_ri_embedding(en_words, te_words)
        ri_path = os.path.join(self.EMBEDDINGS_DIRECTORY, f"{fileName}_ri.npy")
        np.save(ri_path, ri_embedding)

    def _compute_bert_embedding(self, text):
        """Generate BERT embedding"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.cpu().numpy()

    def _split_languages(self, text):
        """Split text into English and Telugu words"""
        words = text.split()
        en_words = [w.lower() for w in words if all(ord(c) < 128 for c in w)]
        te_words = [w for w in words if not all(ord(c) < 128 for c in w)]
        return en_words, te_words

    def _compute_ri_embedding(self, en_words, te_words):
        """Generate Random Indexing embedding"""
        doc_vector = make_index(self.dimension, self.nonzeros)
        
        # Process English words
        for word in en_words:
            if word not in self.en_vocab:
                self.en_vocab[word] = [len(self.en_vectors), 1]
                self.en_vectors.append(np.zeros(self.dimension))
            else:
                self.en_vocab[word][1] += 1
                
        # Process Telugu words
        for word in te_words:
            if word not in self.te_vocab:
                self.te_vocab[word] = [len(self.te_vectors), 1]
                self.te_vectors.append(np.zeros(self.dimension))
            else:
                self.te_vocab[word][1] += 1
                
        return doc_vector