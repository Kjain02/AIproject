import os, sys
sys.path.append(os.path.abspath(os.path.join('./')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from DynamicExtracter.generation_template import get_generation_template  
import asyncio

async def get_template(PDF_PATH):
    return await get_generation_template(PDF_PATH)


if __name__ == '__main__':
    addr = 'src/rag/data/brsr-form.pdf'

    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', addr))
    # addr = os.path.abspath(addr)
    # print(addr)
    print(abs_path)
    asyncio.run(get_template(abs_path))