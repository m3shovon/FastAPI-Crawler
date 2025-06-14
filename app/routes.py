from fastapi import APIRouter, Query
from app.crawler import crawl_website

router = APIRouter()

@router.get("/crawl")
async def crawl(url: str = Query(..., description="The starting URL to crawl")):
    result = await crawl_website(url)
    return {"status": "success", "data": result}
