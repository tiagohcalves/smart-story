import os
import qdrant_client
import google.generativeai as genai
import requests

# Configure Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize Qdrant client
client = qdrant_client.QdrantClient(host="localhost", port=6333)
collection_name = "documents"

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

def retrieve_relevant_chunks(query, top_k=5):
    """Finds the most relevant document chunks from Qdrant."""
    query_embedding = get_embedding(query)

    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )

    relevant_chunks = [hit.payload.get("text", "") for hit in search_results]
    relevant_documents = [hit.payload.get("text", "") for hit in search_results]
    return relevant_chunks, relevant_documents

def chat(query):
    """Processes a user query, retrieves relevant docs, and gets a response from Gemini."""
    relevant_chunks, relevant_documents = retrieve_relevant_chunks(query)

    # TODO: retrieve full text for relevant documents    
    
    prompt = f"Pergunta: {query}\nResposta:"
    if not relevant_chunks:
        print("No relevant information found.")
    else:
        context = "\n\n".join(relevant_chunks)
        print("Context: ", context)
        prompt = f"Use o seguinte contexto para responder a pergunta:\n\n{context}\n\Pergunta: {query}\nResposta:"

    response = model.generate_content(prompt)
    return response.text

# Simple chat loop
while True:
    user_query = input("> Você: ")
    if user_query.lower() in ["exit", "quit"]:
        break
    response = chat(user_query)
    print("\n> Hystorian:", response)
