import os
import uuid
import logging
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "rocky_memory"
CHROMA_DB_DIR = os.environ.get("CHROMA_DB_DIR", "chroma_store")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return _client

def _get_or_create_collection():
    client = get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)

async def store_file(file) -> int:
    try:
        contents = await file.read()
        text = contents.decode("utf-8", errors="ignore")
        # Simple chunking: 500 characters
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        if not chunks:
            return 0

        collection = _get_or_create_collection()
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": file.filename} for _ in chunks]
        
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        logger.info(f"Stored {len(chunks)} chunks for {file.filename}")
        return len(chunks)
    except Exception as e:
        logger.error(f"Memory store failed: {e}")
        raise

def query_memory(prompt: str, n: int = 3) -> str:
    try:
        collection = _get_or_create_collection()
        results = collection.query(
            query_texts=[prompt],
            n_results=n
        )
        
        documents = results.get("documents", [[]])[0]
        return "\n".join(documents)
    except Exception as e:
        logger.error(f"Memory query failed: {e}")
        return ""
