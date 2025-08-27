import os
import time
import numpy as np
import PyPDF2
import asyncio
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src.azure_credentials import *
import random
from langchain.retrievers import BM25Retriever, EnsembleRetriever
import tiktoken
import psutil
from tqdm import tqdm
from langchain_chroma import Chroma
from src.utils.azure_blob_storage import upload_folder_to_container

from src.utils.cosmos_utils import store_cosmos_db_row

EMBEDDINGS_DIR = "rag/embeddings"

# TODO - Shifft to a database

# Ensure the embeddings directory exists
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)



def count_tokens(text, model_name='gpt-3.5-turbo'):
    """
    Counts the number of tokens in a text string using tiktoken.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)

def read_pdf(pdf_path: str):
    """
    Reads a PDF file and extracts text from it.
    Returns a list of tuples: (page_number, page_text)
    """
    try:
        pages = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text() or ""  # Ensure we handle None returns gracefully
                pages.append((page_num + 1, text))
        if not pages:
            raise ValueError("No text could be extracted from the PDF.")
        return pages
    except FileNotFoundError:
        print(f"Error: The file at path '{pdf_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None

def chunk_text(pages, chunk_size=2000, overlap=500):
    """
    Divides the text into chunks of approximately chunk_size tokens, with a specified overlap.
    Processes pages individually, and splits them if necessary.
    Adds page number at the start of each chunk.
    Returns a list of tuples: (chunk_text_with_page_number, page_number)
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = []
        for page_num, text in pages:
            num_tokens = count_tokens(text)
            if num_tokens <= chunk_size:
                # Add page number at the start of the chunk
                chunk_text_with_page_number = f"<page_number>{page_num}<page_number>    {text} "
                chunks.append((chunk_text_with_page_number, page_num))
            else:
                # Split the page text into chunks
                page_chunks = text_splitter.split_text(text)
                for chunk in page_chunks:
                    # Add page number at the start of each chunk
                    chunk_text_with_page_number = f"<page_number>{page_num}<page_number>    {chunk} "
                    chunks.append((chunk_text_with_page_number, page_num))
        if not chunks:
            raise ValueError("No chunks could be generated from the text.")
        
        return chunks
    except Exception as e:
        print(f"An error occurred while chunking the text: {e}")
        return None

async def create_documents(chunks):
    """
    Wraps text chunks into Document objects required by LangChain.
    Each chunk is a tuple: (chunk_text_with_page_number, page_number)
    """
    try:
        documents = [Document(page_content=chunk[0], metadata={'page_number': chunk[1]}) for chunk in chunks]
        if not documents:
            raise ValueError("No documents could be created from the chunks.")
        return documents
    except Exception as e:
        print(f"An error occurred while creating documents: {e}")
        return None


async def save_embeddings(embeddings, filename):
    """
    Saves the embeddings to a .npy file.
    """
    filepath = os.path.join(EMBEDDINGS_DIR, filename)
    if os.path.exists(filepath):
        existing_embeddings = np.load(filepath, allow_pickle=True)
        embeddings = np.concatenate((existing_embeddings, embeddings), axis=0)
    np.save(filepath, embeddings)


async def load_embeddings(filename):
    """
    Loads embeddings from a .npy file if they exist.
    """

    filepath = os.path.join(EMBEDDINGS_DIR, filename)
    if os.path.exists(filepath):
        return np.load(filepath, allow_pickle=True)
    return None


def exponential_backoff_with_jitter(attempt, base=2, cap=60):
    """
    Exponential backoff with jitter for handling rate limiting.
    """
    sleep_time = min(cap, base ** attempt) + random.uniform(0, 1)
    print(f"Sleeping for {sleep_time} seconds due to rate limiting...")
    time.sleep(sleep_time)


async def generate_and_store_embeddings_for_chunks(documents, doc_id):
    """
    Generates embeddings for each chunk and stores them sequentially, with a sleep delay in between.
    """
    embeddings_filename = f"{doc_id}_embeddings.npy"

    # Initialize AzureOpenAIEmbeddings for text-embedding-3-large model
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION
    )

    # Check if embeddings already exist
    existing_embeddings = await load_embeddings(embeddings_filename)
    if existing_embeddings is not None:
        text_embedding_pairs = list(zip([doc.page_content for doc in documents], existing_embeddings))
        return FAISS.from_embeddings(text_embedding_pairs, embeddings)

    all_embeddings = []
    text_embedding_pairs = []
    # fd = open(embeddings_filename, "wb")
    try:
        for i, document in enumerate(tqdm(documents, desc="Processing Documents")):
            attempt = 0
            while True:
                try:
                    # Generate embedding for the chunk
                    chunk_embeddings = embeddings.embed_documents([document.page_content])[0]  
                    text_embedding_pairs.append((document.page_content, chunk_embeddings))
                    
                    # Append to the list of all embeddings
                    all_embeddings.append(chunk_embeddings)
                    
                    # await save_embeddings(np.array(chunk_embeddings), embeddings_filename)
                    break  # If successful, break out of the loop
                except Exception as e:
                    if '429' in str(e):
                        attempt += 1
                        exponential_backoff_with_jitter(attempt)
                    else:
                        raise e

            # Sleep every 100 iterations to handle rate limiting
            if i % 100 == 0:
                time.sleep(1)

        # # Save the embeddings to a .npy file as List[List[float]]
        await save_embeddings(np.array(all_embeddings), embeddings_filename)

        print(f"Saved embeddings for document ID: {doc_id}")

        # Create the FAISS vectorstore from the embeddings

        faiss = FAISS.from_embeddings(text_embedding_pairs, embeddings)

        if not faiss:
            raise ValueError("Failed to build a vectorstore from the embeddings.")
        return faiss

    except Exception as e:
        print(f"An error occurred while generating and storing embeddings: {e}")
        return None




async def instantiate_vectorstore(path_to_file: str | list ): 
    """
    Creates embeddings for a PDF file by chunking the text and generating embeddings for each chunk.
    """
    try:
        pdf_lists = []
        # Check if the  path is a list of paths
        if isinstance(path_to_file, list):
            pdf_lists = path_to_file
        else:
            pdf_lists.append(path_to_file)

        texts = []
        for path in pdf_lists:
            text = read_pdf(path)
            texts.extend(text)
        
        chunks = chunk_text(texts)

        # chunks = chunk_text(text)
        del texts
        print("Total chunks: ", len(chunks))

        if not chunks:
            raise ValueError("No chunks could be generated from the text.")

        # Create Document objects from the chunks
        documents = await create_documents(chunks)
        
    
        print("Created documents")
        if not documents:
            raise ValueError("No documents could be created from the chunks.")

        # return None
        # Generate and store embeddings for the chunks

        if isinstance(path_to_file, list):
            path_to_file = "_".join([os.path.basename(path) for path in path_to_file])

        vectorstore = await generate_and_store_embeddings_for_chunks(documents, os.path.basename(path_to_file))
        if not vectorstore:
            raise ValueError("Failed to generate embeddings for the chunks.")
        # add filter so that it returns page_number as well

        retriever_vectordb = vectorstore.as_retriever(search_kwargs={"k": 15})
        keyword_retriever = BM25Retriever.from_documents(documents)
        keyword_retriever.k = 8
        ensemble_retriever = EnsembleRetriever(retrievers=[retriever_vectordb,keyword_retriever],
                                       weights=[0.75, 0.25])
        del documents
        return ensemble_retriever

    except Exception as e:
        print(f"An error occurred while creating embeddings: {e}")
        return None
    

async def create_vectorstore_chroma(path_to_file: str, vectorstore_address: str, collection_name: str): 
    """
    Creates embeddings for a PDF file by chunking the text and generating embeddings for each chunk.
    """
    try:

        print("Before reading pdf")
        # Read the PDF file
        text = read_pdf(path_to_file)
        print("After reading pdf")
        if not text:
            raise ValueError("No text could be extracted from the PDF.")
        # print("Pdf reading completed...")
        # Chunk the text
        chunks = chunk_text(text)
        del text
        print("Total chunks: ", len(chunks))

        if not chunks:
            raise ValueError("No chunks could be generated from the text.")

        # Create Document objects from the chunks
        documents = await create_documents(chunks)
        
        


        print("Created documents")
        if not documents:
            raise ValueError("No documents could be created from the chunks.")
        

        embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION
        )

        vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=vectorstore_address,  # Where to save data locally, remove if not necessary
        )

        for doc in documents:

            vector_store.add_documents(documents=[doc])
        
        # # Print the Content of the vectorstore
        # data = vector_store._collection.get(include=["documents", "metadatas"])
        # document = data["documents"]
        # metadata = data["metadatas"]

        # # print(documents[0])
        # # print("Metadata: ", metadata[0])
        # # print("Metadata: ", metadata[1])

        # documents = []

        # for doc, meta in zip(document, metadata):
        #     documents.append(Document(page_content=doc, metadata=meta))

        # vector_store = vector_store.as_retriever(search_kwargs={"k": 15})
        # keyword_retriever = BM25Retriever.from_documents(documents)
        # keyword_retriever.k = 8
        # ensemble_retriever = EnsembleRetriever(retrievers=[vector_store,keyword_retriever],
        #                                weights=[0.75, 0.25])
        
        addr = upload_folder_to_container(vectorstore_address, "ChromaVectorStore")

        return (vector_store, addr)
    
    except Exception as e:
        print(f"An error occurred while creating embeddings: {e}")
        return None


async def process_and_store_chunk(embedding_id, chunk_number, chunk_text_indi, embeddings_model):
    """
    Processes a single text chunk: generates its embedding and stores it in CosmosDB.
    """
    try:
        chunk_embedding = await asyncio.to_thread(embeddings_model.embed_documents, [chunk_text_indi])
        created_at = str(time.time())

        return await store_cosmos_db_row(embedding_id, chunk_number, chunk_embedding[0], chunk_text_indi, created_at)

    except Exception as e:
        print(f"Error processing chunk {chunk_number}: {e}")
        return 0  # Return 0 to indicate failure


async def create_vectorstore_cosmos(path_to_file: str, embedding_id: str):
    """
    Reads a PDF, generates text embeddings, and stores them in Cosmos DB asynchronously.
    """
    try:
        text = read_pdf(path_to_file)
        if not text:
            raise ValueError("No text could be extracted from the PDF.")

        chunks = chunk_text(text)
        del text  # Free memory
        print(f"Total chunks: {len(chunks)}")

        if not chunks:
            raise ValueError("No chunks could be generated from the text.")

        # Initialize embedding model only once
        embeddings_model = AzureOpenAIEmbeddings(
            model="text-embedding-3-large",
            azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
            api_key=AZURE_OPENAI_GPT_API_KEY,
            openai_api_version=AZURE_OPENAI_API_VERSION
        )

        # Process embeddings and store in CosmosDB in parallel
        tasks = []
        for chunk_number, (chunk_text_indi, chunk_page) in enumerate(chunks, start=1):
            tasks.append(process_and_store_chunk(embedding_id, chunk_number, chunk_text_indi, embeddings_model))

        results = await asyncio.gather(*tasks)  # Run all tasks in parallel
        print(f"Successfully stored {sum(results)} chunks in Cosmos DB.")
        return {"status": "success", "stored_chunks": sum(results)}

    except Exception as e:
        print(f"Error in create_vectorstore_cosmos: {e}")
        return {"status": "failed", "error": str(e)}


async def embedding_pair(documents, doc_id):
    """
    Generates embeddings for each chunk and stores them sequentially, with a sleep delay in between.
    """
    embeddings_filename = f"{doc_id}_embeddings.npy"

    # Initialize AzureOpenAIEmbeddings for text-embedding-3-large model
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION
    )

    # Check if embeddings already exist
    existing_embeddings = await load_embeddings(embeddings_filename)
    if existing_embeddings is not None:
        text_embedding_pairs = list(zip([doc.page_content for doc in documents], existing_embeddings))
        return text_embedding_pairs

    all_embeddings = []
    text_embedding_pairs = []
    # fd = open(embeddings_filename, "wb")
    try:
        for i, document in enumerate(tqdm(documents, desc="Processing Documents")):
            attempt = 0
            while True:
                try:
                    # Generate embedding for the chunk
                    chunk_embeddings = embeddings.embed_documents([document.page_content])[0]  
                    text_embedding_pairs.append((document.page_content, chunk_embeddings))
                    
                    # Append to the list of all embeddings
                    all_embeddings.append(chunk_embeddings)
                    
                    # await save_embeddings(np.array(chunk_embeddings), embeddings_filename)
                    break  # If successful, break out of the loop
                except Exception as e:
                    if '429' in str(e):
                        attempt += 1
                        exponential_backoff_with_jitter(attempt)
                    else:
                        raise e

            # Sleep every 100 iterations to handle rate limiting
            if i % 100 == 0:
                time.sleep(1)

        # # Save the embeddings to a .npy file as List[List[float]]
        await save_embeddings(np.array(all_embeddings), embeddings_filename)

        print(f"Saved embeddings for document ID: {doc_id}")

        # Create the FAISS vectorstore from the embeddings

        return text_embedding_pairs

    except Exception as e:
        print(f"An error occurred while generating and storing embeddings: {e}")
        return None

async def storing_embeddings(path_to_file: str):
    try:

        print("Before reading pdf")
        # Read the PDF file
        text = read_pdf(path_to_file)
        print("After reading pdf")
        if not text:
            raise ValueError("No text could be extracted from the PDF.")
        # print("Pdf reading completed...")
        # Chunk the text
        chunks = chunk_text(text)
        del text
        print("Total chunks: ", len(chunks))

        if not chunks:
            raise ValueError("No chunks could be generated from the text.")

        # Create Document objects from the chunks
        documents = await create_documents(chunks)
        
        


        print("Created documents")
        if not documents:
            raise ValueError("No documents could be created from the chunks.")

        # Store Documents in the database

        # return None
        # Generate and store embeddings for the chunks
        embedding_pairs = await embedding_pair(documents, os.path.basename(path_to_file))
        if not embedding_pairs:
            raise ValueError("Failed to generate embeddings for the chunks.")

        
        return [documents, embedding_pairs]

    except Exception as e:
        print(f"An error occurred while creating embeddings: {e}")
        return None