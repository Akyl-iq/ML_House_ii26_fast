from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from my_project.database.db import SessionLocal
from my_project.database.models import Region
from my_project.database.schema import RegionOutSchema, RegionInputSchema
from typing import List



region_router = APIRouter(prefix='/region', tags=['Region'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@region_router.post('/', response_model=RegionOutSchema)
async def create(region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = Region(**region.dict())
    db.add(region_db)
    db.commit()
    db.refresh(region_db)
    return region_db


@region_router.get('/',response_model=List[RegionOutSchema])
async def list_region(db: Session = Depends(get_db)):
    return db.query(Region).all()


@region_router.get('/{region_id}',response_model=RegionOutSchema)
async def detail_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id==region_id).first()
    if not region_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return region_db




@region_router.put('/{region_id}', response_model=dict)
async def update_region(region_id: int, region: RegionInputSchema,
                          db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id==region_id).first()
    if not region_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    for region_key, region_value in region.dict().items():
        setattr(region_db,region_key,region_value)

    db.add(region_db)
    db.commit()
    db.refresh(region_db)
    return {'message': 'Категория озгорду'}


@region_router.delete('/', response_model= dict)
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id==region_id).first()
    if not region_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    db.delete(region_db)
    db.commit()
    return {'message': 'Маалымат очурулду'}