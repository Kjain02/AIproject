# Fin Stat Analyser

## Code Structure

```
fin-stat-analyser-main/
│
├── src/
│   ├── extraction.py            
│   ├── score.py                 
│   ├── main.py                 
│   ├── config.py              
│   ├── services/                
│   ├── scrape_people/          
│   ├── rag/                     
│   ├── output/                 
│   └── companies.json          
├── requirements.txt             
├── Readme.md                    
└── .gitignore                   

```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fin-stat-analyser.git
cd fin-stat-analyser

```
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Add company data to `companies.json` file. The JSON should have the following structure:

```json
[
    {
        "isin": "GB0005405286",
        "filepath": "path/to/file.pdf",
        "year": "2020"
    }
]
```

2. Run the main script:

```bash
python src/main.py
```

- The script will extract data from the provided documents and generate a JSON file with the extracted data. It will also update the databse with the extracted data.

## Configuration

- **Azure Credentials** : Ensure that you have the Azure credentials set up in the `src/azure_credentials.py` file.
- **Delays and Timeouts** :  Can be configured in the `src/config.py` file.


## Output

- The extracted data will be stored in the `src/output/` directory in JSON format.


## Key Components

### 1. RAG Pipeline

- Builds a Vector Store from a collection of documents.
- Queries the Vector Store to retrieve relevant documents.
  
Refere to [RAG Pipeline README](src/rag/README.md) for details.

### 2. Open Web Search and Information Extraction Pipeline

- Uses [Azure Bing Entity Search API](https://www.microsoft.com/en-us/bing/apis/bing-entity-search-api) to extract information from the web.
- Processes the extracted information to generate structured data.
- Feeds the structured data to OpenAI to extract relevant information using [Function calling](https://platform.openai.com/docs/guides/function-calling).
  
Refer to [Open Web Search README](src/scrape_people/README.md) for details.
