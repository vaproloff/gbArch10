from fastapi import APIRouter, HTTPException
from db import database, pets
from models.pet import Pet, PetIn

router = APIRouter()


@router.get("/pets/", response_model=list[Pet])
async def get_all():
    query = pets.select()
    return await database.fetch_all(query)


@router.get("/pets/{pet_id}", response_model=Pet)
async def get_by_id(pet_id: int):
    query = pets.select().where(pets.c.id == pet_id)
    fetch = await database.fetch_one(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Pet not found')
    return fetch


@router.post("/pets/", response_model=Pet)
async def create(pet: PetIn):
    query = pets.insert().values(client_id=pet.client_id,
                                 name=pet.name,
                                 birthday=pet.birthday)
    last_record_id = await database.execute(query)
    return {**pet.model_dump(), "id": last_record_id}


@router.put("/pets/{pet_id}", response_model=Pet)
async def update(pet_id: int, new_pet: PetIn):
    query = pets.update().where(pets.c.id == pet_id).values(**new_pet.model_dump())
    fetch = await database.execute(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Pet not found')
    return {**new_pet.model_dump(), "id": pet_id}


@router.delete("/pets/{pet_id}")
async def delete(pet_id: int):
    query = pets.delete().where(pets.c.id == pet_id)
    fetch = await database.execute(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Pet not found')
    return {'message': 'Pet deleted'}
