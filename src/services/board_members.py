import json
import asyncio
import logging
from colorlog import ColoredFormatter
from src.rag.query import find_relevant_chunks
from src.rag.template_query import rag_query
from src.config import config
import time
import os
from src.rag.generate.board_member_details import fetch_board_details
from src.rag.generate.board_remuneration import fetch_bm_remuneration

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

OUTPUT_DIR = "output"

async def board_member_names(vectorstore):
    try:
        query = rag_query['board_member_details']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        board_member_details = await fetch_board_details(relevant_chunks)
        # with open(f"{OUTPUT_DIR}/board_member_details.json", "w") as f:
        #     json.dump(board_member_details, f, indent=4)
        # print("Board member details fetched and saved successfully.")
        return board_member_details
    except Exception as e:
        print(f"Failed to fetch board member details: {e}")
        raise

async def board_member_remuneration(vectorstore, board_member_details):
    try:
        query = rag_query['board_members_remuneration']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        print("Relevant chunks for board member remuneration fetched successfully.")

        print(len(relevant_chunks))
        print(board_member_details)

        board_member_remuneration = await fetch_bm_remuneration(relevant_chunks, board_member_details)
        return board_member_remuneration
    except Exception as e:
        print(f"Failed to fetch board member remuneration details: {e}")
        raise

async def get_board_member_info(vectorstore):
    try:
        board_member_details = await board_member_names(vectorstore)
        names = [member['name'] for member in board_member_details]
        board_member_remuneration_details = await board_member_remuneration(vectorstore, names)

        # merge the two lists based on the board member "name"
        board_member_info = []
        for member in board_member_details:
            for remuneration in board_member_remuneration_details:
                if member['name'] == remuneration['name']:
                    member.update(remuneration)
                    board_member_info.append(member)
                    break
        
        print("Board member information merged and saved successfully.")
        return board_member_info
    except Exception as e:
        print(f"Failed to fetch board member information: {e}")
        raise