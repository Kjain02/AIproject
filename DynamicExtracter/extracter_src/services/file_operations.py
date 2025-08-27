from PyPDF2 import PdfReader
import json
import os, sys
import asyncio
# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import os

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


"""
@brief: Extract data from a PDF file using the LlamaParse library
@param: pdf_path: str: Path to the PDF file
@return: dict: Data extracted from the PDF file

"""

async def extract_with_tables(pdf_path):
    # Set up parser
    parser = LlamaParse(
        result_type="markdown",
        api_key=LLAMA_CLOUD_API_KEY
    )

    file_extractor = {".pdf": parser}

    # Asynchronously load data
    documents = await SimpleDirectoryReader(
        input_files=[pdf_path],
        file_extractor=file_extractor
    ).aload_data()
    
    doc_text = []

    for doc in documents:
        doc_text.append(doc.text_resource.text)

    return doc_text


"""
@brief: Extract text from a PDF file
@param: pdf_path: str: Path to the PDF file
@return: list: List of text chunks extracted from each page of the PDF
"""

def extract_text_from_pdf(pdf_path):
    print("Absoulte path: ", pdf_path)
    reader = PdfReader(pdf_path)
    text_chunks = [page.extract_text() for page in reader.pages]
    print("Created text chunks")
    return text_chunks



"""
@brief: Write data to a file
@param: path: str: Path to the file
@param: data: dict: Data to write to the file
"""

def write_to_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


"""
@brief: Asynchronously write data to a file
@param: path: str: Path to the file
@param: data: dict: Data to write to the file
@param: file_writer_executor: ThreadPoolExecutor: Executor for the file writing operation
"""

async def async_write_to_file(path, data, file_writer_executor):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(file_writer_executor, write_to_file, path, data)




# # Run the function for local testing
# if __name__ == "__main__":
#     import asyncio
#     # asyncio.run(extract_with_tables("/home/somya/Documents/qnext/fin-analysis/DynamicExtracter/extracter_src/documents/brsr-form.pdf"))