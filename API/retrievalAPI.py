from dotenv import load_dotenv
import os
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'inputProcesser'))
from TenglishFormatter import process_user_input
from ri import dsm, make_index, weight_func, remove_centroid

class RetrievalAPI:
    def __init__(self, dimension=300, nonzeros=8, delta=60):
        """Initialize retrieval system"""
        load_dotenv()
        self.NOTES_DIRECTORY = os.getenv("NOTES_DIRECTORY")
        self.EMBEDDINGS_DIRECTORY = os.getenv("EMBEDDINGS_DIRECTORY")
        
        # BERT initialization
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # RI parameters
        self.dimension = dimension
        self.nonzeros = nonzeros
        self.delta = delta

    def find(self, query):
        """Find relevant documents for the query"""
        processed_query = process_user_input(query)
        
        # Generate query embeddings
        bert_query_embedding = self._compute_bert_embedding(processed_query)
        ri_query_embedding = self._compute_ri_embedding(processed_query)
        
        # Load document embeddings
        results = self._compute_similarities(bert_query_embedding, ri_query_embedding)
        return self._get_top_results(results)

    def _compute_bert_embedding(self, text):
        """Generate BERT embedding for query"""
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

    def _compute_ri_embedding(self, text):
        """Generate RI embedding for query"""
        words = text.split()
        doc_vector = make_index(self.dimension, self.nonzeros)
        return doc_vector

    def _compute_similarities(self, bert_query_emb, ri_query_emb):
        """Compute combined similarities"""
        similarities = {}
        
        for filename in os.listdir(self.EMBEDDINGS_DIRECTORY):
            if filename.endswith('_bert.npy'):
                doc_name = filename.replace('_bert.npy', '')
                
                # Load embeddings
                bert_emb = np.load(os.path.join(self.EMBEDDINGS_DIRECTORY, filename))
                ri_emb = np.load(os.path.join(self.EMBEDDINGS_DIRECTORY, f"{doc_name}_ri.npy"))
                
                # Compute similarities
                bert_sim = cosine_similarity(bert_query_emb, bert_emb)[0][0]
                ri_sim = cosine_similarity(ri_query_emb, ri_emb)[0][0]
                
                # Combine similarities (weighted average)
                combined_sim = 0.7 * bert_sim + 0.3 * ri_sim
                similarities[doc_name] = combined_sim
                
        return similarities

    def _get_top_results(self, similarities, top_k=3):
        """Get top k results with content"""
        sorted_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        results = []
        
        for doc_name, similarity in sorted_docs[:top_k]:
            note_path = os.path.join(self.NOTES_DIRECTORY, f"{doc_name}.txt")
            if os.path.exists(note_path):
                with open(note_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    results.append({
                        'note_id': doc_name,
                        'similarity': similarity,
                        'content': content
                    })
                    
        return results