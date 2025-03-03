import json
import requests
import tqdm

import qdrant_client
from qdrant_client.models import PointStruct
import tiktoken  # For token estimation

from database.models.document import Document
from database.connections.sqlite import SQLiteConnection
from database.repositories.document_repository import DocumentRepository

# Initialize Qdrant
client = qdrant_client.QdrantClient(host="localhost", port=6333)
collection_name = "documents"

# Create collection if not exists
client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": 768, "distance": "Cosine"}
)

# Load JSON
db = DocumentRepository(SQLiteConnection())
# Tokenizer for chunking (assuming OpenAI tokenizer works similarly)
tokenizer = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=512, overlap=50):
    """Splits text into overlapping chunks of max `chunk_size` tokens."""
    tokens = tokenizer.encode(text)
    chunks = []
    
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i : i + chunk_size]
        chunks.append(tokenizer.decode(chunk))

    return chunks

def get_embedding(text):
    """Calls Ollama's embedding model."""
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
        if "embedding" not in response.json():
            print(f"Failed to get embedding for: {text}. Response: {response.json()}")
            return None
        return response.json()["embedding"]
    except Exception as e:
        print(f"Failed to get embedding for: {text}. Error: {e}")
        return None

points = []
chunk_id = 0

# Process documents
documents = db.get_all()
for doc in tqdm.tqdm(documents):
    chunks = chunk_text(doc.get_content())

    for chunk in chunks:
        embedding = get_embedding(chunk)
        if embedding is None:
            continue

        points.append(
            PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={"doc_id": doc.id, "text": chunk, "date": doc.timestamp}
            )
        )
        chunk_id += 1

# Store embeddings in Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"Stored {len(points)} chunks in Qdrant!")
