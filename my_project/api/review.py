from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from my_project.database.db import SessionLocal
from my_project.database.models import Review
from my_project.database.schema import ReviewOutSchema, ReviewInputSchema
from typing import List



review_router = APIRouter(prefix='/review', tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@review_router.post('/', response_model=ReviewOutSchema)
async def create(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get('/',response_model=List[ReviewOutSchema])
async def list_review(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/{review_id}',response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return review_db




@review_router.put('/{review_id}', response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema,
                          db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    for review_key, review_value in review.dict().items():
        setattr(review_db,review_key,review_value)

    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return {'message': 'Категория озгорду'}


@review_router.delete('/', response_model= dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    db.delete(review_db)
    db.commit()
    return {'message': 'Маалымат очурулду'}