from fastapi import APIRouter, HTTPException
from db import clients, database
from models.client import Client, ClientIn

router = APIRouter()


@router.get("/clients/", response_model=list[Client])
async def get_all():
    query = clients.select()
    return await database.fetch_all(query)


@router.get("/clients/{client_id}", response_model=Client)
async def get_by_id(client_id: int):
    query = clients.select().where(clients.c.id == client_id)
    fetch = await database.fetch_one(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Client not found')
    return fetch


@router.post("/clients/", response_model=Client)
async def create(client: ClientIn):
    query = clients.insert().values(document=client.document,
                                    surname=client.surname,
                                    first_name=client.first_name,
                                    patronymic=client.patronymic,
                                    birthday=client.birthday)
    last_record_id = await database.execute(query)
    return {**client.model_dump(), "id": last_record_id}


@router.put("/clients/{client_id}", response_model=Client)
async def update(client_id: int, new_client: ClientIn):
    query = clients.update().where(clients.c.id == client_id).values(**new_client.model_dump())
    fetch = await database.execute(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Client not found')
    return {**new_client.model_dump(), "id": client_id}


@router.delete("/clients/{client_id}")
async def delete(client_id: int):
    query = clients.delete().where(clients.c.id == client_id)
    fetch = await database.execute(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Client not found')
    return {'message': 'User deleted'}
