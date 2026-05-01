import os
from qdrant_client import QdrantClient

url = "https://edd9c911-28e1-4db0-ac0a-9018e2fc3a2b.eu-west-1-0.aws.cloud.qdrant.io"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6MTEwODk4NmMtMjU3ZS00NzhlLWI2MTEtZjBkYWY0ZmQzN2E2In0.nqez1_-XRY5gYr5DSsOqgGcAXW_iX3e2ld_-nINThQU"

client = QdrantClient(url=url, api_key=api_key)
collection_name = "rocky_memory"

try:
    count = client.count(collection_name=collection_name).count
    print(f"Points in collection: {count}")
    
    # Peek at the data
    results = client.scroll(collection_name=collection_name, limit=5)[0]
    for r in results:
        print(f"Content: {r.payload.get('text')[:100]}...")
except Exception as e:
    print(f"Error: {e}")
