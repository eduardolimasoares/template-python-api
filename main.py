from fastapi import FastAPI
from app.core.configs import settings
from app.api.api import api_router

app = FastAPI(title='USER API')
app.include_router(api_router, prefix=settings.API_V1)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)


