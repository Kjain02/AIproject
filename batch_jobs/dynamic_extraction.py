######   ADJUST SYS PATH ######

import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)



from src.rag.create import instantiate_vectorstore

import json
import asyncio
import logging
from job_runner import CompanyDynamicExtracter
from job_runner import run_batch_jobs
import os
from job_runner import logger


GRI_TOPIC_LIST = [101, 201, 202, 203, 204, 205, 206, 207, 301, 302, 303, 304, 305, 306, 308, 401, 402, 403,
                 404, 405, 406, 407, 408, 409, 410, 411, 413, 414, 415, 416, 417, 418]




async def main():
    output_dir = "output/extraction"
    with open('input/companies.json', 'r') as jsonfile:
        companies = json.load(jsonfile)

    job_args = []

    companies_filtered = []

    # filter company for this run
    for company in companies:
        if company["nse_symbol"] == "TCS":
            company['vectorstore'] = await instantiate_vectorstore(company['filepath'])
            companies_filtered.append(company)


    # Filtering GRI topics for this run
    # GRI_TOPIC_LIST = [305]


    # Prepare job arguments
    for topic_id in GRI_TOPIC_LIST:
        for company in companies_filtered:
            job_args.append([company['isin'], topic_id, company['vectorstore'], output_dir ])
                

    logger.info(f"Loaded len({job_args}) GRI topics for processing.")

    # Run batch jobs using GriTemplateProcessor
    failed_gri_topics = await run_batch_jobs(
        jobs=job_args,
        job_processor_class=CompanyDynamicExtracter,
    )

    if failed_gri_topics:
        logger.error("Batch processing completed with failures.")
    else:
        logger.info("Batch processing completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())

