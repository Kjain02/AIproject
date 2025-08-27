import json 
import concurrent.futures
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from newspaper import Article
import http.client, urllib.parse
import json
import os

people_list = []

BING_SUBSCRIPTION_KEY = '5ed68024458846f593bdae92062a0127'

def checkParsable(url: str) -> bool:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return True
    except Exception as e:
        return False

async def search(search_type: str, query: str, count: int = 10, 
                      cc: str = 'IN', 
                      mkt: str = 'en-IN', 
                      safeSearch: str = 'Moderate', 
                      freshness: str = 'Week', 
                      offset: int = 0, 
                      textDecorations: bool = True, 
                      textFormat: str = 'HTML', 
                      sortBy: str = 'Relevance') -> dict:
    if not BING_SUBSCRIPTION_KEY:
        raise ValueError("BING_SUBSCRIPTION_KEY is not set. Please add it to the environment variables.")

    try:
        api_wrapper = BingSearchAPIWrapper(
            bing_subscription_key=BING_SUBSCRIPTION_KEY,
            bing_search_url=f"https://api.bing.microsoft.com/v7.0/{search_type}",
            k=count,
            search_kwargs={
                'cc': cc,
                'mkt': mkt,
                'safeSearch': safeSearch,
                'freshness': freshness,
                'count': count,
                'offset': offset,
                'textDecorations': textDecorations,
                'textFormat': textFormat,
                'sortBy': sortBy,
            }
        )
        tool = BingSearchResults(api_wrapper=api_wrapper)
        response = tool.invoke(query)
        response = json.loads(response.replace("'", '"'))
        return response
    except json.JSONDecodeError as e:
        print(f"Failed to parse response JSON: {str(e)}")
        response = []
    except Exception as e:
        print(f"An error occurred while performing the search: {str(e)}")
        response = []
    return response 


async def entity_search(query: str):
    headers = {
        'Ocp-Apim-Subscription-Key': BING_SUBSCRIPTION_KEY,
    }
    params = urllib.parse.urlencode({
        'q': query,
        'mkt': 'en-US',

    })
    try:
        conn = http.client.HTTPSConnection('api.bing.microsoft.com')
        conn.request("GET", f"/v7.0/entities?{params}", "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)

        desc = ""
        urls = []
        if 'entities' in data and 'value' in data['entities']:
            
            entity = data['entities']['value'][0]
            if 'description' in entity:
                desc = entity['description']
            # return desc, urls
            if 'contractualRules' in entity:
                for rule in entity['contractualRules']:
                    if 'targetPropertyName' in rule and rule['targetPropertyName'] == 'description' and 'url' in rule:
                        urls.append(rule['url'])
        return desc, urls
    except Exception as e:
        print(f"An error occurred while fetching entities: {str(e)}")
        return " ", []


def parse_article(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return ""


async def search_people_on_web(query: str, company: str):
    # Ensure the directory exists
    os.makedirs("./people_dump", exist_ok=True)
    
    # Open the file in append mode
    with open(f"./people_dump/{query}.txt", "a") as f:
        # Perform the entity search
        desc, urls = await entity_search(query + " " + company)
        
        # Initialize an empty string to store all URL content combined
        all_url_content = ""
        
        # Check if URLs were found
        if urls:
            for url in urls:
                if checkParsable(url):
                    # Parse the content from the URL
                    url_content = parse_article(url)
                    # Convert both the URL and the parsed content to strings and write to the file
                    f.write(str(url) + "\n")
                    f.write(str(url_content) + "\n")
                    # Append this content to the combined content
                    all_url_content += str(url_content) + " "
        
        # Combine the description and all URL content
        final_content = str(desc) + " " + all_url_content
        
        # Write the final content to the file
        f.write(final_content + "\n")
    

    # Return the final content
    return final_content