import summary
from typing import Optional
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="OpenAIKey")

def get_api_key(
        api_key_header: str = Security(api_key_header),
) -> str:
    if len(api_key_header)>0:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "world"}

@app.get("/summary")
async def get_summary(web_url: Optional[str] = None,api_key: str = Security(get_api_key)):
    sum = summary.generate_summary(api_key,web_url)
    return {"summary": sum}