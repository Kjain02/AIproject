# Retrieval Augmented Generation (RAG) over Financial Statements

## Key Functions

This module exposes two top-level functions to interact with the RAG pipeline:

1. **`instantiate_vectorstore`**: Creates embeddings for a PDF file by chunking the text and generating embeddings for each chunk.
2. **`find_relevant_chunks`**: Finds the most relevant document chunks for a given query using the generated vectorstore.

### 1. `instantiate_vectorstore`

```python
async def instantiate_vectorstore(path_to_file: str) -> Optional[VectorStore]:
    """
    Creates embeddings for a PDF file by chunking the text and generating embeddings for each chunk.
    """
```
**Parameters**:
- `path_to_file` (str): Path to the PDF file to be processed.
  
**Returns**:
- `Optional[VectorStore]`: A VectorStore object containing the embeddings, or None if the process fails.

**Description**:
This function performs the following steps:

- Reads the PDF file and extracts its text content.
- Chunks the extracted text into smaller segments.
- Creates Document objects from these chunks.
- Generates embeddings for each chunk using Azure OpenAI's text-embedding-3-large model.
- Stores the embeddings in a FAISS vectorstore.

The function includes error handling and implements an **exponential backoff strategy with jitter** to handle rate limiting.

### 2. `find_relevant_chunks`
```python
async def find_relevant_chunks(query: str, vectorstore: VectorStore, top_k: int = 5) -> List[str]:
    """
    Finds the most relevant document chunks for a given query using the generated vectorstore.
    """
```

**Parameters**:
- `query` (str): The query string for which relevant chunks are to be retrieved.
- `vectorstore` (VectorStore): The VectorStore object containing the embeddings of the document chunks.
- `top_k` (int): The number of relevant chunks to retrieve (default is 5).

**Returns**:
- `List[str]`: A list of the most relevant document chunks based on the query, or an empty list if no relevant chunks are found.

**Description**:
This function performs a similarity search on the vectorstore using the provided query. It returns the top_n most relevant chunks of text from the original document.


## Usage

To use the RAG pipeline:

1. Instantiate a VectorStore for a given PDF file using `instantiate_vectorstore`.
   
```python
vectorstore = await instantiate_vectorstore("path/to/your/financial_statement.pdf")
```

2. Find the most relevant chunks for a query using `find_relevant_chunks`.

```python
query = "What is the revenue for the year 2020?"
relevant_chunks = await find_relevant_chunks(query, vectorstore)
```

3. Process the relevant chunks as needed for downstream tasks.

## Implementation Details

- The module uses Azure OpenAI's text-embedding-3-large model for generating embeddings.
- Embeddings are stored in .npy files in a directory specified by `EMBEDDINGS_DIR`.
- The text is split into chunks using `RecursiveCharacterTextSplitter` with a default chunk size of 10000 and overlap of 200.
- The module implements caching of embeddings to avoid regenerating them for the same document.
- Rate limiting is handled using an exponential backoff strategy with jitter.