from fastapi import FastAPI
from services.extractor import extract_data_using_newspaper

app = FastAPI()

@app.get("/extract/")
async def root(url: str):
    """
        Extract Text API
        :param url: URL of the article to be parsed
        :returns: Response
    """
    
    return extract_data_using_newspaper(url)