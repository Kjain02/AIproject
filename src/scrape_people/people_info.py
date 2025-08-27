import json
from scrape_people.extract_field import gpt_extract_field
from scrape_people.web_search_people import search_people_on_web

async def search_people(person, company):
    """
    Searches for a person on the web and returns the search results.
    """
    
    web_data = await search_people_on_web(person, company)
    if len(web_data) > 10:

        print(f"Found information about {person} on web")
        gpt_response = await gpt_extract_field(web_data, person)
        return gpt_response
    else:
        print("No search results found.\n")
        return ""



