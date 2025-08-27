import asyncio
import random
import logging
import uvloop
from abc import ABC, abstractmethod
from src.db import read_gri_template, write_gri_extraction_table
from src.rag.new_generate.function_call import llm_generate
from src.rag.query import find_relevant_chunks
from src.rag.create import instantiate_vectorstore
import os
import json


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# Logging configuration
class CustomFormatter(logging.Formatter):
    """Custom formatter for colored logging."""
    COLORS = {
        'DEBUG': "\033[90m",     # Grey
        'INFO': "\033[92m",      # Green
        'WARNING': "\033[93m",   # Yellow
        'ERROR': "\033[91m",     # Red
        'CRITICAL': "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{self.RESET}"

# Setting up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = CustomFormatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Retry and job processing logic (same as in your example)
MAX_RETRY = 7  # Default maximum retries
INITIAL_DELAY = 2  # Default initial delay for retry in seconds

class JobProcessor(ABC):
    """Abstract base class for job processors."""
    
    @abstractmethod
    async def process(self, job):
        """Process a single job."""
        pass

class GriTemplateProcessor(JobProcessor):
    """Processor for GRI template generation."""

    def __init__(self, output_dir, update_db_flag):
        self.output_dir = output_dir
        self.update_db_flag = update_db_flag

    async def process(self, job):
        """Process a single GRI topic using get_generation_template."""
        try:
            from DynamicExtracter.generate_gri_template import get_generation_template
            filepath, file_name, topic, division, topic_id = job
            job_args = [filepath, file_name, topic, division, topic_id]
            common_args = [self.output_dir, self.update_db_flag]
            result = await get_generation_template(job_args, common_args)
            return result is not None  # Return True if processing succeeds
        except Exception as e:
            logger.error(f"Failed to process GRI topic {job}: {e}")
            return False


class CompanyDynamicExtracter(JobProcessor):
    """Extract the information for a company for any given template."""

    def __init__(self):
        self.template = None
    
    def verify_generation(self, extracted_data):
        """Verify the extracted data."""

        #TODO: Implement verification logic for genrated output

        if not extracted_data:
            return False
        
        return True

    async def process_section(self, section, vectorstore, output_dir = None, isin = None):
        """Process a single section asynchronously."""
        try:
            # Find relevant chunks
            relevant_chunks = await find_relevant_chunks(section['rag_prompt'], vectorstore)
            

            tool_call = []
            tool_call.append(section['tool_template'])

            # Generate data using LLM
            extracted_data = await llm_generate(
                relevant_chunks,
                tool_call,
                section['system_prompt'],
                section['user_prompt']
            )
            
            # Verify the extracted data
            if not self.verify_generation(extracted_data):
                logger.warning(f"Verification failed for section {section['section_name']}")
                return None

            # create a directory for each company
            os.makedirs(f"{output_dir}/{isin}", exist_ok=True)

            if output_dir is not None:
                with open(f"{output_dir}/{isin}/{section['section_name']}.json", 'w') as jsonfile:
                    json.dump({
                        'tool_template': section['tool_template'],
                        'extracted_data': extracted_data
                    }, jsonfile, indent=4)

            # Add section metadata
            extracted_data['section_name'] = section['section_name']
            extracted_data['section_description'] = section['section_description']
            
            return extracted_data
        except Exception as e:
            logger.error(f"Error processing section {section['section_name']}: {e}")
            return None


    async def process(self, job):
        """Process a single company using get_company_info."""
        try:
            isin, template_id, vectorstore, output_dir = job


            if vectorstore is None:
                logger.error(f"Vectorstore not found for company {isin}")
                return False

            # Read template information
            template = await read_gri_template(template_id)
            sections = template['format']

            # Process all sections concurrently
            tasks = [self.process_section(section, vectorstore, output_dir) for section in sections]
            results = await asyncio.gather(*tasks)
            
            # Filter out failed sections
            total_extracted_data = [data for data in results if data is not None]
            
            if(len(total_extracted_data) == 0):
                logger.error(f"No data extracted for company {isin} using template {template_id}")
                return False                
            
            # Write results to the extraction table
            await write_gri_extraction_table(isin, template_id, total_extracted_data)
            logger.info(f"Successfully processed company {job}")
            return True
        except Exception as e:
            logger.error(f"Failed to process company {job}: {e}")
            return False



# Job processing functions

async def process_job(job, job_processor):
    """Process a single job using the provided JobProcessor."""
    try:
        response = await job_processor.process(job)

        if not response:
            logger.warning(f"Job {job} returned None.")
            return False
        else:
            logger.info(f"Successfully processed job: {job}")
            return True
    except Exception as e:
        logger.error(f"Failed to process job {job}: {e}")
        return False

async def retry_with_backoff(job, retry_count, job_processor):
    """Retry a job with exponential backoff and jitter."""
    delay = INITIAL_DELAY * (2 ** retry_count) + random.uniform(0, 1)
    if retry_count > 0:
        logger.warning(f"Retrying job {job} after {delay:.2f} seconds (Retry {retry_count+1}/{MAX_RETRY})")
        await asyncio.sleep(delay)
    return await process_job(job, job_processor)

async def handle_job_with_retries(job, job_processor, max_retry=MAX_RETRY):
    """Handle a job with retries."""
    for retry_count in range(max_retry):
        success = await retry_with_backoff(job, retry_count, job_processor)
        if success:
            return True
    logger.error(f"Max retries reached for job: {job}")
    return False


async def run_batch_jobs(jobs, job_processor_class, **processor_args):
    """Run a batch of jobs concurrently."""
    job_processor = job_processor_class(**processor_args)  # Instantiate the processor
    tasks = [handle_job_with_retries(job, job_processor) for job in jobs]
    results = await asyncio.gather(*tasks)

    # Log failed jobs
    failed_jobs = [jobs[i] for i, success in enumerate(results) if not success]
    if failed_jobs:
        logger.error(f"{len(failed_jobs)} jobs failed: {failed_jobs}")
    else:
        logger.info("All jobs processed successfully.")

    return failed_jobs
