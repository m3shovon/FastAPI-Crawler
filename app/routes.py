from fastapi import APIRouter, Query
from app.crawler import crawl_website, extract_page_content

router = APIRouter()

@router.get("/crawl")
async def crawl(url: str = Query(..., description="The starting URL to crawl")):
    result = await crawl_website(url)
    return {"status": "success", "data": result}

@router.get("/extract-content")
async def extract_content(url: str = Query(..., description="URL to extract content from")):
    content = await extract_page_content(url)
    return {"status": "success", "url": url, "content": content}