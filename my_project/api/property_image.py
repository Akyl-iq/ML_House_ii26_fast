from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from my_project.database.db import SessionLocal
from my_project.database.models import PropertyImage
from my_project.database.schema import PropertyImageInputSchema, PropertyImageOutSchema
from typing import List



property_image_router = APIRouter(prefix='/property_image', tags=['PropertyImage'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@property_image_router.post('/', response_model=PropertyImageOutSchema)
async def create(property_image: PropertyImageInputSchema, db: Session = Depends(get_db)):
    property_image_db = PropertyImage(**property_image.dict())
    db.add(property_image_db)
    db.commit()
    db.refresh(property_image_db)
    return property_image_db


@property_image_router.get('/',response_model=List[PropertyImageOutSchema])
async def list_property_image(db: Session = Depends(get_db)):
    return db.query(PropertyImage).all()


@property_image_router.get('/{property_image_id}',response_model=PropertyImageOutSchema)
async def detail_property_image(property_image_id: int, db: Session = Depends(get_db)):
    property_image_db = db.query(PropertyImage).filter(PropertyImage.id==property_image_id).first()
    if not property_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return property_image_db




@property_image_router.put('/{property_image_id}', response_model=dict)
async def update_property_image(property_image_id: int, property_image: PropertyImageInputSchema,
                          db: Session = Depends(get_db)):
    property_image_db = db.query(PropertyImage).filter(PropertyImage.id==property_image_id).first()
    if not property_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    for property_image_key, property_image_value in property_image.dict().items():
        setattr(property_image_db,property_image_key,property_image_value)

    db.add(property_image_db)
    db.commit()
    db.refresh(property_image_db)
    return {'message': 'Категория озгорду'}


@property_image_router.delete('/', response_model= dict)
async def delete_property_image(property_image_id: int, db: Session = Depends(get_db)):
    property_image_db = db.query(PropertyImage).filter(PropertyImage.id==property_image_id).first()
    if not property_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    db.delete(property_image_db)
    db.commit()
    return {'message': 'Маалымат очурулду'}