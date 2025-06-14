from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Web Crawler API")
app.include_router(router)
