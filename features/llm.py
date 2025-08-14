from typing import List, Dict
import nltk
from nltk.corpus import wordnet
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from datetime import datetime
import numpy as np
import time
import logging

logging.basicConfig(
    filename="llm.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

nltk.download('wordnet')

class LLM:
    def __init__(self):
        print("Initializing LLM...")
        self.vectorizer = TfidfVectorizer()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("LLM initialized successfully.\n")
    
    #Query Expansion
    def expand_query(self, query: str) -> str:
        print(f"Expanding query: {query}")
        synonyms = set()
        for word in query.split():
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.add(lemma.name())
        expanded_query = query + ' ' + ' '.join(synonyms)
        print(f"Query expanded to: {expanded_query}\n")
        return expanded_query

    #Normalizing Document Length
    def normalize_length(self, documents: List[Dict[str, str]], target_length: int = 4000) -> List[Dict[str, str]]:
        print(f"Normalizing document length to {target_length} words...")
        for doc in documents:
            words = doc['full_text'].split()
            if len(words) > target_length:
                doc['full_text'] = ' '.join(words[:target_length])
        print(f"Document lengths normalized to {target_length} words.\n")
        return documents

    #Temporal Relevance
    def evaluate_temporal_relevance(self, documents: List[Dict[str, str]]) -> np.ndarray:
        print("Evaluating temporal relevance of documents...")
        current_year = datetime.now().year
        years = np.array([
            current_year - datetime.strptime(doc.get("year", str(current_year)), '%Y').year
            for doc in documents
        ])
        epsilon = 1e-6
        relevance_scores = 1 / (np.log1p(years) + epsilon)
        print(f"Temporal relevance scores calculated: {relevance_scores}\n")
        return relevance_scores

    def evaluate_relevance(self, query: str, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        print(f"Evaluating relevance for query: {query}\n")
        start_time = time.time()
        
        expanded_query = self.expand_query(query)

        documents = self.normalize_length(documents)

        # TF-IDF Vectorization
        print("Performing TF-IDF vectorization...")
        texts = [doc['full_text'] for doc in documents]
        texts.append(expanded_query)
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        query_tfidf = tfidf_matrix[-1]
        tfidf_scores = cosine_similarity(query_tfidf, tfidf_matrix[:-1]).flatten()
        print(f"TF-IDF scores: {tfidf_scores}\n")

        # Embedding and Semantic Search
        print("Generating sentence embeddings and performing semantic search...")
        embeddings = self.embedding_model.encode(texts, convert_to_tensor=True)
        query_embedding = embeddings[-1]
        embedding_scores = cosine_similarity(
            query_embedding.detach().numpy().reshape(1, -1),
            embeddings[:-1].detach().numpy()
        ).flatten()
        print(f"Semantic similarity scores: {embedding_scores}\n")

        # Combine Scores
        combined_scores = (0.5 * tfidf_scores + 0.5 * embedding_scores)
        print(f"Combined relevance scores: {combined_scores}\n")

        # Temporal Relevance Scores
        temporal_relevance_scores = self.evaluate_temporal_relevance(documents)

        # Final Scores
        final_scores = combined_scores * 0.7 + temporal_relevance_scores * 0.1
        print(f"Final combined scores (including temporal relevance): {final_scores}\n")

        # Rank Documents
        ranked_indices = np.argsort(final_scores)[::-1]
        ranked_documents = [documents[i] for i in ranked_indices]

        end_time = time.time()
        relevance_time = end_time - start_time
        print(f"Time taken for relevance evaluation: {relevance_time:.2f} seconds\n")
        
        print("Relevance evaluation complete.\n")
        return ranked_documents

    def get_top_n_relevant_documents(self, query: str, documents: List[Dict[str, str]], n: int = 5) -> List[Dict[str, str]]:
       print(f"Processing documents to find the top {n} most relevant to '{query}'...")
       ranked_docs = self.evaluate_relevance(query, documents)
       top_docs = ranked_docs[:n]
       print(f"Top {n} relevant documents selected.\n")
       return top_docs
   