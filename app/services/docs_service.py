import re
from config import openai_client, qdrant, EMBEDDING_MODEL, COLLECTION_NAME

def query_qdrant(query, collection_name, vector_name="article", top_k=5):
    embedded_query = (
        openai_client.embeddings.create(
            input=query,
            model=EMBEDDING_MODEL,
        )
        .data[0]
        .embedding
    )

    return qdrant.search(
        collection_name=collection_name,
        query_vector=(vector_name, embedded_query),
        limit=top_k,
    )

def query_docs(query):
    print(f"Searching knowledge base with query: {query}")
    query_results = query_qdrant(query, collection_name=COLLECTION_NAME)
    output = []

    for article in query_results:
        output.append((
            article.payload["title"],
            article.payload["text"],
            article.payload["url"]
        ))

    if output:
        title, content, _ = output[0]
        response = f"Title: {title}\nContent: {content}"
        truncated_content = re.sub(
            r"\s+", " ",
            content[:50] + "..." if len(content) > 50 else content
        )
        print("Most relevant article title:", truncated_content)
        return {"response": response}
    
    print("No results")
    return {"response": "No results found."}
