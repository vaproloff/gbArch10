import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from db import database
from routers import client, pet, consultation

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(client.router, tags=["clients"])
app.include_router(pet.router, tags=["pets"])
app.include_router(consultation.router, tags=["consultations"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
