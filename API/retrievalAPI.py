from dotenv import load_dotenv
import os
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'inputProcesser'))
from TenglishFormatter import process_user_input
from ri import dsm ,make_index, weight_func, remove_centroid

class RetrievalAPI:
    def __init__(self, dimension=300, nonzeros=8, delta=60):
        """Initialize retrieval system"""
        load_dotenv()
        self.NOTES_DIRECTORY = os.getenv("NOTES_DIRECTORY")
        self.EMBEDDINGS_DIRECTORY = os.getenv("EMBEDDINGS_DIRECTORY")
        self.VEC_EN_DIR = os.getenv("VEC_EN_DIR")
        self.VEC_TE_DIR = os.getenv("VEC_TE_DIR")
        
        # Create directories if they don't exist
        for directory in [self.NOTES_DIRECTORY, self.EMBEDDINGS_DIRECTORY, 
                         self.VEC_EN_DIR, self.VEC_TE_DIR]:
            os.makedirs(directory, exist_ok=True)
        
        # BERT initialization
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Dimensions and parameters
        self.bert_dimension = 768
        self.ri_dimension = dimension
        self.nonzeros = nonzeros
        self.delta = delta
        
        # Load vocabularies
        self._load_vocabularies()

    def find(self, query):
        try:
            processed_query = self._process_query(query)
            print(f"Processing query: '{processed_query}'")
            
            bert_query_emb = self._compute_bert_embedding(processed_query)
            ri_query_emb = self._compute_ri_embedding(processed_query)
            
            results = self._compute_similarities(bert_query_emb, ri_query_emb)
            
            if not results:
                print("No matching results found.")
                return []
            
            return self._get_top_results(results)
            
        except Exception as e:
            print(f"Error in find method: {str(e)}")
            raise

    def _get_top_results(self, similarities, top_k=3):
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
            return embedding.reshape(1, self.bert_dimension)

    def _compute_ri_embedding(self, text):
        """Compute RI embeddings separately for English and Telugu"""
        # Split languages
        words = text.split()
        en_words = [w.lower() for w in words if all(ord(c) < 128 for c in w)]
        te_words = [w for w in words if not all(ord(c) < 128 for c in w)]
        
        # Compute English embedding
        en_vector = np.zeros(self.ri_dimension)
        for word in en_words:
            if word in self.en_vocab:
                idx = self.en_vocab[word][0]
                en_vector += self.en_vectors[idx]
        
        # Compute Telugu embedding
        te_vector = np.zeros(self.ri_dimension)
        for word in te_words:
            if word in self.te_vocab:
                idx = self.te_vocab[word][0]
                te_vector += self.te_vectors[idx]
        
        # Combine vectors
        combined_vector = en_vector + te_vector
        if np.any(combined_vector):
            combined_vector = combined_vector / np.linalg.norm(combined_vector)
        
        return combined_vector.reshape(1, self.ri_dimension)


    def _compute_similarities(self, bert_query_emb, ri_query_emb):
        similarities = {}
        bert_weight = 0.7
        ri_weight = 0.3

        print(f"\nProcessing query embeddings:")
        print(f"BERT query shape: {bert_query_emb.shape}")
        print(f"RI query shape: {ri_query_emb.shape}")

        for filename in os.listdir(self.NOTES_DIRECTORY):
            if filename.endswith('.txt'):
                try:
                    doc_name = filename.replace('.txt', '')
                    bert_path = os.path.join(self.EMBEDDINGS_DIRECTORY, f"{doc_name}_bert.npy")
                    en_path = os.path.join(self.VEC_EN_DIR, f"{doc_name}_ri.npy")
                    te_path = os.path.join(self.VEC_TE_DIR, f"{doc_name}_ri.npy")
                    
                    if all(os.path.exists(p) for p in [bert_path, en_path, te_path]):
                        # Load embeddings
                        bert_emb = np.load(bert_path)
                        en_emb = np.load(en_path)
                        te_emb = np.load(te_path)
                        
                        # Combine RI embeddings
                        ri_emb = en_emb + te_emb
                        if np.any(ri_emb):
                            ri_emb = ri_emb / np.linalg.norm(ri_emb)
                        
                        # Normalize BERT embedding
                        bert_norm = np.linalg.norm(bert_emb)
                        if bert_norm > 0:
                            bert_emb = bert_emb / bert_norm
                        
                        # Compute similarities
                        bert_sim = cosine_similarity(bert_query_emb, bert_emb)[0][0]
                        ri_sim = cosine_similarity(ri_query_emb, ri_emb.reshape(1, -1))[0][0]
                        
                        print(f"\nProcessing document: {doc_name}")
                        print(f"BERT similarity: {bert_sim:.4f}")
                        print(f"RI similarity: {ri_sim:.4f}")
                        
                        # Combine similarities
                        combined_sim = bert_weight * bert_sim + ri_weight * ri_sim
                        
                        if combined_sim > 0.05:
                            similarities[doc_name] = combined_sim
                            print(f"Match found! Combined similarity: {combined_sim:.4f}")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    continue

        return similarities


    def _process_query(self, query):
        """Process query text"""
        try:
            return process_user_input(query)
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return query
        
        
    
    def _load_vocabularies(self):
        """Load existing vocabularies"""
        self.en_vocab = {}
        self.te_vocab = {}
        self.en_vectors = []
        self.te_vectors = []
        
        # Load English vocabulary
        en_path = os.path.join(self.VEC_EN_DIR, "vocab.npz")
        if os.path.exists(en_path):
            data = np.load(en_path, allow_pickle=True)
            self.en_vocab = data['vocab'].item()
            self.en_vectors = data['vectors']
            
        # Load Telugu vocabulary
        te_path = os.path.join(self.VEC_TE_DIR, "vocab.npz")
        if os.path.exists(te_path):
            data = np.load(te_path, allow_pickle=True)
            self.te_vocab = data['vocab'].item()
            self.te_vectors = data['vectors']