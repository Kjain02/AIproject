# Open Web Search and Information Extraction Pipeline

## Key Functions


1. **`search_people`**: Searches for people on the web using the Bing Entity Search API and extracts relevant information.

### 1. `search_people`

```python
async def search_people(person: str, company: str) -> List[Dict[str, Any]]:
    """
    Searches for people on the web using the Bing Entity Search API and extracts relevant information.
    """
```

**Parameters**:
- `person` (str): The name of the person to search for.
- `company` (str): The name of the company associated with the person.

**Returns**:
- `List[Dict[str, Any]]`: A dictionary containing relevant information about the person, or an empty list if no information is found.

***Description***:
This function serves as the entry point for the people search process. It performs a web search for the specified person and company, and if sufficient results are found, it uses GPT to extract relevant information from the web data.

2. **`search_people_on_web`**:
```python
async def search_people_on_web(query: str, company: str) -> str:
    """
    Performs a web search for the specified person and company, collecting and storing relevant information.
    """
```

**Parameters**:
- `query` (str): The search query for the person.
- `company` (str): The name of the company associated with the person.

**Returns**:
- `str`: A string containing the extracted information about the person.

***Description***:
This function uses the Bing Search API and entity search to find information about the person. It also parses and stores the content from relevant URLs.


3. ** `gpt_extract_fields`**:
```python
async def gpt_extract_field(chunk: str, person_name: str) -> dict:
    """
    Uses GPT to extract relevant information about the person from the web data.
    """

```

**Parameters**:

- `chunk` (str): The text chunk to be processed.
- `person_name` (str): The name of the person to search for.

**Returns**:
- `dict`: A dictionary containing the extracted information about the person.

***Description***:
This function leverages the Azure OpenAI GPT-3.5 model to analyze the web data and extract pertinent information about the specified person using few-shot prompting and function calling.

## **Usage**
To use the Open Web Search and Information Extraction Pipeline:

```python
person_name = "John Doe"
company_name = "Acme Corp"
result = await search_people(person_name, company_name)
print(result)
```

## Implementation Details

- The module uses the Bing Search API for web searches and entity recognition.
- It leverages the newspaper library to parse and extract content from web pages.
- The Azure OpenAI GPT-3.5 model is used for information extraction and analysis.
- Search results and extracted information are stored in text files within a people_dump directory.
- The module implements few-shot prompting and function calling to guide the GPT model in extracting    specific information fields.

### Extraction Fields

The following fields are extracted for each person:

``` json
{
  "name": {
    "type": "string",
    "description": "The full name of the person, as mentioned in the document. This field is essential for identifying the individual."
  },
  "designation": {
    "type": "string",
    "description": "The specific designation or role held by the person in the current organization. This description should include the full title and any relevant responsibilities."
  },
  "age": {
    "type": "integer",
    "description": "The current age of the person, if mentioned. This should be an accurate representation based on the provided text."
  },
  "gender": {
    "type": "string",
    "description": "The gender of the person as identified in the text. Ensure that this field is only included if explicitly stated."
  },
  "remuneration": {
    "type": "string",
    "description": "Details about the remuneration or compensation package of the person in the current organization. Include specifics such as salary, bonuses, and other forms of compensation if available."
  },
  "educational_background": {
    "type": "string",
    "description": "A detailed summary of the person's educational qualifications, including degrees, institutions attended, and any special recognitions or honors received."
  },
  "professional_background": {
    "type": "string",
    "description": "An overview of the person's professional history, including previous positions, organizations, and relevant achievements in those roles."
  },
  "years_experience_same_industry": {
    "type": "integer",
    "description": "The total number of years the person has spent working within the same industry. This should be a calculated figure based on the person's career timeline."
  },
  "experience_different_industry": {
    "type": "string",
    "description": "Information about the person's experience in different industries. This should include the nature of roles and contributions made in those industries."
  },
  "expertise": {
    "type": "array",
    "description": "A list of specific areas of expertise the person possesses. This should be based on their educational background, professional experiences, and any recognized skills.",
    "items": {
      "type": "string",
      "description": "A distinct area of expertise, such as finance, marketing, or leadership."
    }
  }
}
```
