import sys
import os

sys.path.append(os.path.abspath(os.path.join('./')))
# print(sys.path)

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from src.schemas import gettingfileresponse, gettingtemplaterequest, extraction_query
router = APIRouter()
from src.config import extraction_config
from src.db import supabase_extraction

from src.azure_credentials import *
from src.utils.cosmos_utils import cosmos_get_relevant_chunks
import asyncio
import uuid

from src.utils.azure_blob_storage import download_blob_from_uri, upload_file_to_container
from src.utils.format_generation import get_template

from src.rag.create import storing_embeddings, create_vectorstore_chroma, create_vectorstore_cosmos
from langchain_community.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever

from fastapi.encoders import jsonable_encoder
from src.rag.new_generate.function_call import llm_generate

import json
from datetime import datetime

import re

def sanitize_name(name):
    # Remove invalid characters and replace with an underscore
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Truncate to a maximum of 63 characters
    name = name[:63]
    # Ensure it starts and ends with an alphanumeric character
    name = re.sub(r'^[-_]+', '', name)
    name = re.sub(r'[-_]+$', '', name)
    return name

async def bg_process(file_id, company_document_id):
    try:
        result = await asyncio.to_thread(
                lambda : supabase_extraction.table(extraction_config['files'])
                .select("*")
                .eq('file_id', file_id)
                .execute()
            )

        result = result.dict()

        file_uri = result['data'][0]['file_uri']
        print(file_uri)
        # file_status = result['data'][0]['status']
        file_id = result['data'][0]['file_id']
        organization_id = result['data'][0]['organization_id']

        collection_name = f"{company_document_id}_{str(uuid.uuid4())}"

        pdf_name = f"{file_id}_{company_document_id}.pdf"

        
        collection_name = sanitize_name(collection_name)
    
        pdf_addr = f"src/rag/data/" + pdf_name
        resp = download_blob_from_uri(file_uri, pdf_addr)

        if resp == 0:
            return {"status": "failed", "detail": "Failed to download the document."}

        print("Pdf Stored Successfully")

        embedding_model = {"model_name" : "text-embedding-3-large"}   # Will be changed later depending on the model(dynamically)
        embedding_model = json.dumps(embedding_model)
        
        print("Just before storing embeddings")
        chroma_store_addr = f"src/rag/data/{file_id}_{company_document_id}_chromavectorstore"
        
        tuple_res = await create_vectorstore_chroma(pdf_addr, chroma_store_addr,collection_name)

        if tuple_res is None:
            raise ValueError("Failed to create embeddings.")
        
        vectorstore = tuple_res[0]
        blob_storage_link = tuple_res[1]

        embeddings_id = f"embedding_{file_id}_{company_document_id}_{str(uuid.uuid4())}"

        print("Just before storing embeddings")

        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['embeddings'])
            .insert({'embedding_id':embeddings_id,'organization_id':organization_id,'embedding_model':embedding_model, 'status': 'success','created_at':datetime.now().isoformat(),'company_document_id':company_document_id,'collection_name':collection_name,'blob_storage_link':blob_storage_link, 'file_id':file_id})
            .execute()
        )

        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['files'])
            .update({'status': 'success'})
            .eq('file_id', file_id)
            .execute()
        )

        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['company_documents'])
            .update({'status': 'success'})
            .eq('company_document_id', company_document_id)
            .execute()
        )

        print("Background Task Completed")

        return {"status": "success", "detail": "Embeddings created and stored successfully."}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "failed", "detail": str(e)}


# @router.post("/create_embeddings")
async def create_embeddings_test(fileresponse : gettingfileresponse, background_tasks: BackgroundTasks):
    try:
        file_id = fileresponse.file_id
        company_document_id = fileresponse.company_document_id
        print(file_id)
        print(company_document_id)
        background_tasks.add_task(bg_process, file_id, company_document_id)
        print("Background Task Added")
        return {"status": "success", "detail": "Embeddings created and stored successfully."}
    except Exception as e:
        return {"status": "failed", "detail": str(e)}


async def test_bg_process(file_id, company_document_id):
    try:
        print("Inside Test Background Task")
        result = await asyncio.to_thread(
                lambda : supabase_extraction.table(extraction_config['files'])
                .select("*")
                .eq('file_id', file_id)
                .execute()
            )
        print("Result: ", result)
        result = result.dict()

        file_uri = result['data'][0]['file_uri']
        print(file_uri)
        # file_status = result['data'][0]['status']
        file_id = result['data'][0]['file_id']
        organization_id = result['data'][0]['organization_id']

        pdf_name = f"{file_id}_{company_document_id}.pdf"
    
        pdf_addr = f"src/rag/data/" + pdf_name
        resp = download_blob_from_uri(file_uri, pdf_addr)

        if resp == 0:
            return {"status": "failed", "detail": "Failed to download the document."}

        print("Pdf Stored Successfully")
        embeddings_id = f"embedding_{file_id}_{company_document_id}_{str(uuid.uuid4())}"
        stats = await create_vectorstore_cosmos(pdf_addr, embeddings_id)
        print("Stats: ", stats)
        if stats['status'] == "failed":
            return stats
        
        embedding_model = {"model_name" : "text-embedding-3-large"}   # Will be changed later depending on the model(dynamically)
        embedding_model = json.dumps(embedding_model)
        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['embeddings'])
            .insert({'embedding_id':embeddings_id,'organization_id':organization_id,'embedding_model':embedding_model, 'status': 'success','created_at':datetime.now().isoformat(),'company_document_id':company_document_id, 'file_id':file_id})
            .execute()
        )

        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['files'])
            .update({'status': 'success'})
            .eq('file_id', file_id)
            .execute()
        )

        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['company_documents'])
            .update({'status': 'success'})
            .eq('company_document_id', company_document_id)
            .execute()
        )

        print("Background Task Completed")
        return {"status": "success", "detail": "Embeddings created and stored successfully."}
    except Exception as e:
        print("Error: ", str(e))
        return {"status": "failed", "detail": str(e)}


@router.post("/create_embeddings")
async def create_embeddings(fileresponse : gettingfileresponse, background_tasks: BackgroundTasks):
    # try:
        file_id = fileresponse.file_id
        company_document_id = fileresponse.company_document_id
        print(file_id)
        print(company_document_id)
        background_tasks.add_task(test_bg_process, file_id, company_document_id)
        print("Background Task Added")
        return {"status": "success", "detail": "Embeddings created and stored successfully."}
    # except Exception as e:
    #     return {"status": "failed", "detail": str(e)}

# from DynamicExtracter.generate_gri_template import get_generation_template

# from src.rag.query import find_relevant_chunks
# async def check():
#     template = open("final1.json", "r")

#     template = json.load(template)

#     file_path = "src/rag/data/test1.pdf"
#     vectorstore = await create_vectorstore_chroma(file_path, "src/rag/data/test1_chromavectorstore")
#     vectorstore
#     test_section = template[0]
#     print(test_section)
#     relevant_chunks = await find_relevant_chunks(test_section['rag_prompt'], vectorstore)
#     relevant_chunks

async def bg_process_template(file_id, format_category, format_name):
    suparow = await asyncio.to_thread(
        lambda : supabase_extraction.table(extraction_config['files'])
        .select("*")
        .eq('file_id', file_id)
        .execute()
    )

    # Handling the response
    if not suparow.data:  # Instead of suparow['data']
        print("File not found.")
        return {"status": "failed", "detail": "File not found."}

    suparow = suparow.dict()
    # print("Suparow: ", suparow)
    organization_id = suparow['data'][0]['organization_id']
    # print(organization_id)
    file_uri = suparow['data'][0]['file_uri']
    pdf_addr = f"src/rag/data/templatefiles/{file_id}_{str(uuid.uuid4())}.pdf"
    # create directory if not exists
    if not os.path.exists("src/rag/data/templatefiles"):
        os.makedirs("src/rag/data/templatefiles")
    # Create Address for the Template File
    print(pdf_addr)
    resp = download_blob_from_uri(file_uri, pdf_addr)
    if resp == 0:
        return {"status": "failed", "detail": "Failed to download the document."}

    # pdf_addr = "src/rag/data/templatefiles/file_fdcac7c7-86b6-49a6-93ce-4ee79b9a68ff_b2a11129-fe67-4695-bf39-c7f5e78cbc87.pdf"
    # organization_id = "organization_1"
    template = await get_template(pdf_addr)
    # Update the Template in the Database]
    with open(f"src/rag/data/templatefiles/{file_id}.json", "w") as f:
        json.dump(template, f)
    
    blob_link_template = upload_file_to_container(f"src/rag/data/templatefiles/{file_id}.json", "templatefiles")

    if blob_link_template == 0:
        return {"status": "failed", "detail": "Failed to upload the template."}

    template = json.dumps(template)
    format_id = f"format_{file_id}_{str(uuid.uuid4())}"
    await asyncio.to_thread(
        lambda : supabase_extraction.table(extraction_config['formats'])
        .insert({'format_id':format_id,'organization_id':organization_id,'format_category':format_category, 'format_name': format_name,'created_on':datetime.now().isoformat(),'file_id':file_id,'schema':template,'status':'success','blob_template_uri':blob_link_template})
        .execute()
    )

    return {"status": "success", "detail": "Template created and stored successfully."}

@router.post("/create_template")
async def create_template(template_request: gettingtemplaterequest, background_tasks: BackgroundTasks):
    try:
        file_id = template_request.file_id
        format_category = template_request.format_category
        format_name = template_request.format_name
        # print(file_id, format_category, format_name)
        
        print("Background Task Added")
        background_tasks.add_task(bg_process_template, file_id, format_category, format_name)

        return {"status": "success", "detail": "Template created and stored successfully."}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "failed", "detail": str(e)}


async def process_section(section, embedding_id, index, total_output):
    """
    Processes a single section by retrieving relevant chunks and generating text.
    Appends the result at the correct index in total_output.
    """
    relevant_chunks = await cosmos_get_relevant_chunks(embedding_id, section['rag_prompt'], top_k_results=5)
    
    section['tool_template']['function']['name'] = "function_gri_topic"
    tool_call = [section['tool_template']]

    generated_text = await llm_generate(relevant_chunks, tool_call, section['system_prompt'], section['user_prompt'])
    
    total_output[index] = generated_text
    print("Generated Text: ", generated_text)

async def bg_process_data_extraction(company_document_id: str, format_id: str, format_file_id : str):
    try:

        # Get the format schema
        format_schema = await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['formats'])
            .select("*")
            .eq('format_id', format_id)
            .execute()
        )

        if not format_schema.data:
            return {"status": "failed", "detail": "Format not found."}

        format_schema = format_schema.dict()
        format_schema_uri = format_schema['data'][0]['blob_template_uri']

        save_json = f"src/rag/data/{format_file_id}.json"
        resp = download_blob_from_uri(format_schema_uri, save_json)
        if resp == 0:
            return {"status": "failed", "detail": "Failed to download the format schema."}
        
        # Get the embeddings_id from the company_document_id
        embeddings_id = await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['embeddings'])
            .select("embedding_id")
            .eq('company_document_id', company_document_id)
            .execute()
        )

        if not embeddings_id.data:
            return {"status": "failed", "detail": "Embeddings not found."}
        
        embeddings_id = embeddings_id.dict()
        embedding_id = embeddings_id['data'][0]['embedding_id']

        company_details = await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['company_documents'])
            .select("*")
            .eq('company_document_id', company_document_id)
            .execute()
        )

        if not company_details.data:
            return {"status": "failed", "detail": "Company Document not found."}
        
        company_details = company_details.dict()

        company_id = company_details['data'][0]['company_id']
        organization_id = company_details['data'][0]['organization_id']

        
        
        template = open(save_json, "r")
        template = json.load(template)
        print(type(template))
        # total_output = []
        total_output = [None] * len(template)
        # for section in template:
        #     # print(section)
        #     relevant_chunks = await (cosmos_get_relevant_chunks(embedding_id, section['rag_prompt'], top_k_results=5))
        #     tool_call = []
        #     section['tool_template']['function']['name'] = "function_gri_topic"

        #     tool_call.append(section['tool_template'])
        #     generated_text = await (llm_generate(relevant_chunks,tool_call ,section['system_prompt'],section['user_prompt']))
        #     total_output.append(generated_text)
        #     print("Generated Text: ", generated_text)

        tasks = [asyncio.create_task(process_section(section, embedding_id, idx, total_output)) for idx, section in enumerate(template)]

        await asyncio.gather(*tasks)

        extraction_id = f"extraction_{company_document_id}_{format_file_id}_{str(uuid.uuid4())}"
        with open(f"src/rag/data/{extraction_id}.json", "w") as f:
            json.dump(total_output, f)

        
        res = upload_file_to_container(f"src/rag/data/{extraction_id}.json", "extractionfiles")

        if res == 0:
            return {"status": "failed", "detail": "Failed to upload the extraction file."}
        
        await asyncio.to_thread(
            lambda : supabase_extraction.table(extraction_config['extractions'])
            .insert({'extraction_id':extraction_id,'company_id':company_id,'organization_id':organization_id, 'company_document_id':company_document_id,'format_id':format_id,'created_at':datetime.now().isoformat(), 'extraction_blob_uri':res})
            .execute()
        )

    except Exception as e:
        print("Problem in API Call")
        print(f"Error: {str(e)}")
        return {"status": "failed", "detail": str(e)}

@router.post("/data_extraction")
async def data_extraction(extraction_query: extraction_query , background_tasks: BackgroundTasks):
    try:
        company_document_id = extraction_query.company_document_id
        format_id = extraction_query.format_id
        format_file_id = extraction_query.format_file_id

        
        background_tasks.add_task(bg_process_data_extraction, company_document_id, format_id, format_file_id)
        # Get the embeddings from the embeddings_id from the Cosmos DB

        return {"status": "success", "detail": "Data Extraction Completed."}



    except Exception as e:
        return {"status": "failed", "detail": str(e)}




# if __name__ == "__main__":
#     asyncio.run(check())