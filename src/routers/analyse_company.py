from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from src.database_update.users.users_table import update_user_table
import string
import random
import os
from src.schemas import AnalyseDocumentSchema, AnalyseDocumentByIsinSchema
import hashlib
from batch_jobs.extraction_with_source import process_company
router = APIRouter()
from src.db import read_user_table_entry


PDF_PATH = 'src/rag/data/'

import os
import random
import string
from fastapi import HTTPException
import httpx

def create_file_name(str1: str) -> str:

    combined_str = str1
    hash_object = hashlib.sha256()
    hash_object.update(combined_str.encode('utf-8'))
    return hash_object.hexdigest()


async def download_document(download_url: str) -> str:
    try:
        print("Starting file download...")

        async with httpx.AsyncClient() as client:
            response = await client.get(download_url)
            response.raise_for_status()
        
        print("Download successful.")

        # Create a random string for the file name
        name = create_file_name(download_url)
        
        # save the file in the current directory
        with open(f"{name}.pdf", 'wb') as file:
            file.write(response.content)

        print(f"File written successfully at {name}.pdf")

        return f"{name}.pdf"

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error occurred: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download document: {e}")


async def process_document(file_path,file_id, user_id, url, company_id):
    
    """Process the document after downloading."""
    print("Processing document...")

    print(f"File path: {file_path}")    

    try:
        # Update the user table with the extracted data
        vectorstore, company_year = await update_user_table(file_path,file_id, user_id)
        company = {
            "filepath": file_path,
            "isin": company_id,
            "year": company_year,
            "user_id": user_id
        }
        # Add the process_company function as a background task
        await process_company(company)
        print("Document processed successfully.")
    except Exception as e:
        print(f"Failed to process document: {e}")
    
    # Delete the file after processing
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete file: {e}")


@router.post('/analyse_document')
async def analyse_document(payload: AnalyseDocumentSchema, background_tasks: BackgroundTasks):
    try:
        print("Analyse document endpoint called.")
        data = payload.dict()
        download_url = data.get('download_url')
        user_id = data.get('user_id')    
        file_id = data.get('company_id')
        company_id = data.get('company_id')
        if not download_url:
            raise HTTPException(status_code=400, detail="No download URL provided.")

        # Download the document
        file_path = await download_document(download_url)
        # Add the process_document function as a background task
        background_tasks.add_task(process_document, file_path, file_id, user_id, download_url, company_id)
        # Return an 200 response
        return {"message": "Document processing started."   }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")
    

# @router.post('/analyse_isin')
# async def analyse_isin(payload:AnalyseDocumentByIsinSchema, background_tasks: BackgroundTasks):
#     try:
#         print("Analyse ISIN endpoint called.")
#         data = payload.dict()
#         id = data.get('file_id')
#         user_id = data.get('user_id')

#         user_table_entry = await read_user_table_entry(user_id)

#         if user_table_entry is None:
#             raise HTTPException(status_code=404, detail="User not found.")
        
#         download_link = None
#         for company in user_table_entry['company_files']:
#             if company['id']  == id:
#                 download_link = company['url']
#                 break
        
#         if not download_link:
#             raise HTTPException(status_code=404, detail="ISIN not found.")
        
#         # Download the document
#         file_path = await download_document(download_link)

#         company = {
#             "filepath": file_path,
#             "isin": id,
#             "year": "2024",
#             "user_id": user_id
#         }

#         # Add the process_company function as a background task
#         background_tasks.add_task(process_company, company)
#         return {"message": "Document processing started."}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to process ISIN: {e}")