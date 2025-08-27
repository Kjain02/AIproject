from pydantic import BaseModel

class AnalyseDocumentSchema(BaseModel):
    file_id : str
    download_url : str
    user_id : str
    company_id : str

class AnalyseDocumentByIsinSchema(BaseModel):
    file_id : str
    user_id : str


class gettingfileresponse(BaseModel):
    file_id : str
    company_document_id : str

class gettingtemplaterequest(BaseModel):
    file_id : str
    format_category : str
    format_name : str
    
class extraction_query(BaseModel):
    company_document_id : str
    format_id : str
    format_file_id : str