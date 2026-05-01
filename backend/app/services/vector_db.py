import os
import uuid
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

COLLECTION_NAME = "rocky_memory"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
VECTOR_SIZE = 384  # bge-small-en-v1.5 output dimension

_embedder = None


def get_embedder() -> TextEmbedding:
    global _embedder
    if _embedder is None:
        try:
            _embedder = TextEmbedding(model_name=EMBED_MODEL)
        except Exception:
            _embedder = None
            raise
    return _embedder


def get_client() -> QdrantClient:
    url = os.environ.get("QDRANT_URL")
    api_key = os.environ.get("QDRANT_API_KEY")
    if not url or not api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment.")
    return QdrantClient(url=url, api_key=api_key)


def _ensure_collection(client: QdrantClient) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


async def store_file(file) -> int:
    try:
        contents = await file.read()
        text = contents.decode("utf-8", errors="ignore")
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        if not chunks:
            logger.info("No chunks stored for %s in %s", file.filename, COLLECTION_NAME)
            return 0

        embedder = get_embedder()
        embeddings = list(embedder.embed(chunks))

        client = get_client()
        _ensure_collection(client)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={"text": chunk, "source": file.filename},
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.info(
            "Stored %s chunks in %s for %s",
            len(points),
            COLLECTION_NAME,
            file.filename,
        )
        return len(points)
    except Exception as e:
        logger.error("Memory store failed: %s", e, exc_info=True)
        raise


def query_memory(prompt: str, n: int = 3) -> str:
    try:
        embedder = get_embedder()
        query_vector = list(embedder.embed([prompt]))[0].tolist()

        client = get_client()
        _ensure_collection(client)

        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=n,
        )
        points = getattr(results, "points", results)
        logger.info("Memory context retrieved: %s results", len(points))
        return "\n".join([r.payload.get("text", "") for r in points])
    except Exception as e:
        logger.error("Memory query failed: %s", e, exc_info=True)
        return ""
