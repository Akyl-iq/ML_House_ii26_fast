from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from my_project.database.db import SessionLocal
from my_project.database.models import District
from my_project.database.schema import DistrictInputSchema, DistrictOutSchema
from typing import List



district_router = APIRouter(prefix='/district', tags=['District'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@district_router.post('/', response_model=DistrictOutSchema)
async def create(district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = District(**district.dict())
    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return district_db


@district_router.get('/',response_model=List[DistrictOutSchema])
async def list_district(db: Session = Depends(get_db)):
    return db.query(District).all()


@district_router.get('/{district_id}',response_model=DistrictOutSchema)
async def detail_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id==district_id).first()
    if not district_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return district_db




@district_router.put('/{district_id}', response_model=dict)
async def update_district(district_id: int, district: DistrictInputSchema,
                          db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id==district_id).first()
    if not district_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    for district_key, district_value in district.dict().items():
        setattr(district_db,district_key,district_value)

    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return {'message': 'Категория озгорду'}


@district_router.delete('/', response_model= dict)
async def delete_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id==district_id).first()
    if not district_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    db.delete(district_db)
    db.commit()
    return {'message': 'Маалымат очурулду'}