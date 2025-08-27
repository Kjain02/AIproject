from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os, sys
import asyncio
import uuid
sys.path.append(os.path.abspath(os.path.join('../..')))

from src.azure_credentials import *
import json
import os

from langchain_openai import AzureOpenAIEmbeddings

PRIMARY_CONNECTION_STRING = AZURE_COSMOS_PRIMARY_CONNECTION_STRING

client = CosmosClient.from_connection_string(PRIMARY_CONNECTION_STRING)
database = client.get_database_client(AZURE_COSMOS_DATABASE_NAME)
container = database.get_container_client(AZURE_COSMOS_CONTAINER_NAME)

embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION
    )

async def get_embedding(text: str):
    """
    Retrieves the embedding of the given text using Azure OpenAI.
    :param text: The text to embed.
    :return: The embedding of the text.
    """
    try:
        embedding = embeddings.embed_documents([text])[0]
        return embedding

    except Exception as e:
        print(f"An error occurred while retrieving the embedding: {e}")
        return None

# embedding_id , organization_id , embedding_model , embedding , chunk_content , embedding_criteria , created_at , company_document_id , status

#  Our New Keys for cosmos DB are:
# embedding_id , chunk_number , embedding , chunk_content , created_at , status

# container_settings = container.read()
# print(container_settings["indexingPolicy"])

async def store_cosmos_db_row(embedding_id: str, chunk_number: int, embedding: list, chunk_content: str, created_at: str):
    """
    Stores a chunk in CosmosDB asynchronously.
    """
    try:
        unique_id = f"{embedding_id}_{chunk_number}_{uuid.uuid4()}"
        item = {
            "id": unique_id,  # Required by Cosmos DB
            "embedding_id": embedding_id,
            "chunk_number": chunk_number,
            "embedding": embedding,
            "chunk_content": chunk_content,
            "created_at": created_at,
            "status": "success"
        }

        # Store in CosmosDB using async thread
        await asyncio.to_thread(container.create_item, body=item)
        print(f"Item stored: {unique_id}")
        return 1  # Success

    except Exception as e:
        print(f"Error storing document: {e}")
        return 0  # Failure



# Query the container
async def query_cosmos_db(query_embedding: list, query_text: str, embedding_id:str, top_k_results:int = 5):
    """
    Queries the Cosmos DB container for the top-k results based on the query embedding and text.
    :param query_embedding: The embedding of the query text.
    :param query_text: The query text.
    :param top_k_results: The number of top-k results to return.
    :param embedding_id: The embedding_id to filter the results.
    :return: A list of top-k documents matching the query.
    """
    try:
        # Do Hybrid search on rows where the embedding_id = embedding_id
        print(f"Querying Cosmos DB for top-{top_k_results} results...")
        query = f"""
        SELECT TOP {top_k_results} *
        FROM c
        WHERE c.embedding_id = "{embedding_id}"
        ORDER BY RANK RRF(VectorDistance(c.embedding, {query_embedding}), FullTextScore(c.chunk_content, "{query_text}"))
        """
        parameters = [{"name": "@embedding_id", "value": embedding_id}]

        # print(f"Query: {query}")
        # print(type(query_embedding))
        # print(type(query_text))
        # print(type(embedding_id))
        # print(type(top_k_results))

        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=False  # Required for multi-partition queries
        ))

        print(f"Found {len(items)} items.")

        chunks = []

        if items:
            for item in items:
                print(item["chunk_number"])
                chunks.append(item["chunk_content"])
                # print(f"Chunk: {item['chunk_content']}")

        return chunks
    except Exception as e:
        print(f"Error querying documents: {e}")
        return []
    

async def cosmos_get_relevant_chunks(embedding_id: str, query: str, top_k_results: int = 5):
    """
    Retrieves the most relevant chunks from Cosmos DB for the given query.
    :param embedding_id: The embedding_id to filter the results.
    :param query: The query text.
    :param top_k_results: The number of top-k results to return.
    :return: A list of top-k relevant chunks.
    """
    try:
        # Get the embedding of the query text
        query_embedding = await get_embedding(query)
        if not query_embedding:
            return []

        # Query Cosmos DB for the top-k results
        items = await query_cosmos_db(query_embedding, query, embedding_id, top_k_results)
        return items

    except Exception as e:
        print(f"An error occurred while retrieving relevant chunks: {e}")
        return []

# async def main():
#     query_text = " CUSTOMER\nENGAGEMENT\nSales, Project Management,  \nDelivery, Quality Management\nTalent Acquisition\nTalent Engagement\nTalent DevelopmentResearch & Innovation\nProducts & Platforms\nServices & Solutions\nValue\n Sources of funds from business \noperations, financing or investing \nactivitiesFinancial capital\nOperations\nPartners \nTechnology and \nCo-Innovation Network (COIN)\nContextual\nKnowledgeCustomer\nGoodwill/Brand\nValue/CSR/TaxesStakeholder\nPayout, ReservesSocial Capital \nNatural Capital Human CapitalIntellectual Capital\nInvestors, Customers, Employees, Communities Goodwill\nRenewable and Non-renewable Resources\nmotivation of employees\nSkills, competencies, \ncapabilities, knowledge and Domain knowledge\nContextual knowledge\nIntellectual PropertyTCS Integrated Business Model\nValue Creation using the Five Capitals\nTCS Integrated Business Model  \n15\nIntegrated Annual"
#     embedding_id = "embedding_file_3bda781b-f666-411a-88da-0efb18e57de7_company_doc_08fcf7fa-c3f0-4c97-9c62-c4ea7044f5f6_4a82f9bd-7ddb-4ce5-8c7a-bb01e2230067"
#     top_k_results = 5

#     query_embedding = await get_embedding(query_text)
#     # query_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
#     # print(query_embedding)
#     results = await query_cosmos_db(query_embedding, query_text, embedding_id, top_k_results)
    
#     # for item in results:
#     #     print(item["chunk_content"])

# if __name__ == "__main__":
#     asyncio.run(main())