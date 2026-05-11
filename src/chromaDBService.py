import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="documents")


def add_documents(chunks, embeddings):
    ids = []
    for _ in chunks:
        ids.append(str(uuid.uuid4()))

    collection.add(embeddings=embeddings, documents=chunks, ids=ids)


def search_documents(query_embedding, top_k=3):
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return results
