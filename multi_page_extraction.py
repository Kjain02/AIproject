import sys
import os

sys.path.append(os.path.abspath("/DynamicExtracter"))

from DynamicExtracter.generate_gri_template import get_generation_template
from DynamicExtracter.gri.gri_topics import extract_gri_topics


from src.rag.create import instantiate_vectorstore
from src.rag.query import find_relevant_chunks

from src.rag.new_generate.function_call import llm_generate

import json
import asyncio

from concurrent.futures import ThreadPoolExecutor


file_writer_executor = ThreadPoolExecutor()

PDF_PATH = 'DynamicExtracter/extracter_src/documents/topics_101.pdf'


async def section_generation():
    await extract_gri_topics(PDF_PATH, file_writer_executor)


async def multi_source_extraction():
    template = await get_generation_template()



if __name__ == "__main__":
    asyncio.run(multi_source_extraction())
    # asyncio.run(section_generation())