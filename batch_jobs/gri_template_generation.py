######   ADJUST SYS PATH ######

import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)



import json
import asyncio
import logging
from job_runner import GriTemplateProcessor
from job_runner import run_batch_jobs
import os
from job_runner import logger


async def main():

    with open('input/gri_topics.json', 'r') as jsonfile:
        gri_topics = json.load(jsonfile)
    
    output_dir = "output/gri_templates"
    update_db_flag = True

    # Prepare job arguments
    job_args = [
        [topic['filepath'], topic['filepath'].replace('.pdf', ''), topic['topic'], topic['division'], int(topic['id'])]
        for topic in gri_topics 
    ]

    logger.info(f"Loaded len({job_args}) GRI topics for processing.")

    # Run batch jobs using GriTemplateProcessor
    failed_gri_topics = await run_batch_jobs(
        jobs=job_args,
        job_processor_class=GriTemplateProcessor,
        output_dir=output_dir,
        update_db_flag=update_db_flag
    )

    if failed_gri_topics:
        logger.error(f"Batch processing completed with failures. Number of failed topics: {len(failed_gri_topics)}")
    else:
        logger.info("Batch processing completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
