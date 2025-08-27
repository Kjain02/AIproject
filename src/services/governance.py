import json
import asyncio
import logging
from colorlog import ColoredFormatter
from src.rag.query import find_relevant_chunks
from src.rag.template_query import rag_query
from src.config import config
import time

from src.rag.generate.board_structure_independence import fetch_board_structure_independence
from src.rag.generate.executive_compensation import fetch_executive_compensation
from src.rag.generate.shareholder_rights_transparency import fetch_shareholder_rights_transparency
from src.rag.generate.audit_risk_management import fetch_audit_risk_management
from src.rag.generate.ethical_business_practices import fetch_ethical_business_practices
from src.rag.generate.succession_planning_leadership_stability import fetch_succession_planning_leadership_stability
from src.rag.generate.stakeholder_engagement import fetch_stakeholder_engagement

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

OUTPUT_DIR = "output"
filename = "rag/data/Sample-Statements-20240823T132542Z-001/Sample-Statements/2023-24.pdf"

async def stakeholder_engagement(vectorstore):
    try:
        query = rag_query['stakeholder_engagement']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        stakeholder_engagement_details = await fetch_stakeholder_engagement(relevant_chunks)
        print("Stakeholder engagement data fetched successfully.")
        return stakeholder_engagement_details
    except Exception as e:
        print(f"Failed to fetch stakeholder engagement data: {e}")
        raise

async def succession_planning_leadership_stability(vectorstore):
    try:
        query = rag_query['succession_planning_leadership_stability']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        succession_planning_details = await fetch_succession_planning_leadership_stability(relevant_chunks)
        print("Succession planning and leadership stability data fetched successfully.")
        return succession_planning_details
    except Exception as e:
        print(f"Failed to fetch succession planning and leadership stability data: {e}")
        raise

async def board_structure_independence(vectorstore):
    try:
        query = rag_query['board_structure_independence']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        board_structure_details = await fetch_board_structure_independence(relevant_chunks)
        print("Board structure and independence data fetched successfully.")
        return board_structure_details
    except Exception as e:
        print(f"Failed to fetch board structure and independence data: {e}")
        raise

async def executive_compensation(vectorstore):
    try:
        query = rag_query['executive_compensation']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        executive_compensation_details = await fetch_executive_compensation(relevant_chunks)
        print("Executive compensation data fetched successfully.")
        return executive_compensation_details
    except Exception as e:
        print(f"Failed to fetch executive compensation data: {e}")
        raise

async def shareholder_rights_transparency(vectorstore):
    try:
        query = rag_query['shareholder_rights_transparency']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        shareholder_rights_details = await fetch_shareholder_rights_transparency(relevant_chunks)
        print("Shareholder rights and transparency data fetched successfully.")
        return shareholder_rights_details
    except Exception as e:
        print(f"Failed to fetch shareholder rights and transparency data: {e}")
        raise

async def audit_risk_management(vectorstore):
    try:
        query = rag_query['audit_risk_management']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        audit_risk_details = await fetch_audit_risk_management(relevant_chunks)
        print("Audit and risk management data fetched successfully.")
        return audit_risk_details
    except Exception as e:
        print(f"Failed to fetch audit and risk management data: {e}")
        raise

async def ethical_business_practices(vectorstore):
    try:
        query = rag_query['ethical_business_practices']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        ethical_business_practices_details = await fetch_ethical_business_practices(relevant_chunks)
        print("Ethical business practices data fetched successfully.")
        return ethical_business_practices_details
    except Exception as e:
        print(f"Failed to fetch ethical business practices data: {e}")
        raise

async def get_governance_data(vectorstore):
    try:
        
        results = await asyncio.gather(
            board_structure_independence(vectorstore),
            executive_compensation(vectorstore),
            shareholder_rights_transparency(vectorstore),
            audit_risk_management(vectorstore),
            ethical_business_practices(vectorstore),
            succession_planning_leadership_stability(vectorstore),
            stakeholder_engagement(vectorstore)
        )
        board_structure_data, executive_compensation_data, shareholder_rights_data, audit_risk_data, ethical_business_data, succession_planning_data, stakeholder_engagement_data = results

        governance_data = {
            "board_structure_data": board_structure_data,
            "executive_compensation_data": executive_compensation_data,
            "shareholder_rights_data": shareholder_rights_data,
            "audit_risk_data": audit_risk_data,
            "ethical_business_data": ethical_business_data,
            "succession_planning_data": succession_planning_data,
            "stakeholder_engagement_data": stakeholder_engagement_data
        }
        print("Governance data fetched successfully.")
        return governance_data
    except Exception as e:
        print(f"Failed to fetch governance data: {e}")
        raise