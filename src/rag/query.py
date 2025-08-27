async def find_relevant_chunks(query, ensemble_retriever, top_n=5):
    """
    Finds the most relevant document chunks for the input query using ChromaDB.
    Returns the top_n most relevant chunks.
    """

    try:
        docs_rel = ensemble_retriever.get_relevant_documents(query)
        docs_rel = [doc.page_content for doc in docs_rel]
        return docs_rel
    except Exception as e:
        print(f"An error occurred while retrieving relevant chunks: {e}")
        return []
