import logging
import requests
from sentence_transformers import SentenceTransformer
import faiss
from bs4 import BeautifulSoup
import numpy as np

logger = logging.getLogger(__name__)

# Initialize the SentenceTransformer model for embeddings
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = None  # Placeholder for FAISS index
documents = []  # Placeholder for the scraped documents

def scrape_github_doc(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_lines = [line.strip() for line in soup.get_text().splitlines() if line.strip()]
        return "\n".join(content_lines)
    else:
        logger.error(f"Failed to retrieve content from {url} with status code {response.status_code}")
        return None
    
def build_faiss_index(documents):
    embeddings = embedding_model.encode(documents, convert_to_tensor=False)
    # Create a FAISS index
    global faiss_index
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    # Add embeddings to the index
    faiss_index.add(np.array(embeddings))

def retrieve_context(transcript: str, k: int = 3):
    query_embedding = embedding_model.encode([transcript], convert_to_tensor=False)
    _, top_k_indices = faiss_index.search(np.array(query_embedding), k)
    return [documents[idx] for idx in top_k_indices[0]]

def init_rag():
    url = "https://github.com/MystenLabs/mysten-app-docs/blob/main/mysten-sui-wallet.md"
    doc_content = scrape_github_doc(url)
    
    if doc_content:
        documents = doc_content.splitlines()  # Split the scraped content into lines for processing
        build_faiss_index(documents)

