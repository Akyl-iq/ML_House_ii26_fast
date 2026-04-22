from sqlalchemy import Integer, String, Enum, DateTime, Date, ForeignKey, Text, SmallInteger, Boolean, Float
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .db import Base
from typing import Optional,List
from enum import Enum as PyEnum
from datetime import datetime, date

class RoleChoices(str, PyEnum):
    seller ='seller',
    buyer = 'buyer'


class PropertyType(str, PyEnum):
    apartment = 'apartment',
    house =  'house',
    studio = 'studio'


class  ConductionType(str, PyEnum):
    подсамоделку =  'под самоделку',
    евроремонт = 'евроремонт',
    хорошее = 'хорошее',
    среднее = 'среднее',
    недостроено = 'не достроено'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    phone_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), nullable=True, default=RoleChoices.buyer)
    data_register: Mapped[date] = mapped_column(Date, default=date.today)

    property: Mapped[List['Property']] = relationship(back_populates='seller',
                                                      cascade='all, delete-orphan')

    buyer_review: Mapped[List['Review']] = relationship(back_populates='buyer', foreign_keys='Review.buyer_id',
                                                      cascade='all, delete-orphan')

    owner_review: Mapped[List['Review']] = relationship(back_populates='owner', foreign_keys='Review.owner_id',
                                                      cascade='all, delete-orphan')

    refresh_token: Mapped[List['RefreshToken']] = relationship(back_populates='user',
                                                               cascade='all, delete-orphan')

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user: Mapped[UserProfile] = relationship(back_populates='refresh_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow())



class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_name: Mapped[str] = mapped_column(String(32))

    city: Mapped[List['City']] = relationship(back_populates='region',
                                              cascade='all, delete-orphan')

    reg_property: Mapped[List['Property']] = relationship(back_populates='region_property',
                                                      cascade='all, delete-orphan')


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(32))
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    region: Mapped[Region] = relationship(back_populates='city')

    ci_property: Mapped[List['Property']] = relationship(back_populates='city_property',
                                                         cascade='all, delete-orphan')

    district: Mapped[List['District']] = relationship(back_populates='city',
                                                      cascade='all, delete-orphan')

class District(Base):
    __tablename__ = 'district'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(back_populates='district')
    district_name: Mapped[str] = mapped_column(String(32))

    property: Mapped[List['Property']] = relationship(back_populates='district',
                                                      cascade='all, delete-orphan')

class Property(Base):
    __tablename__ = 'property'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType), nullable=True, default=PropertyType.house)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    region_property: Mapped[Region] = relationship(back_populates='reg_property')
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city_property: Mapped[City] = relationship(back_populates='ci_property')
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'))
    district: Mapped[District] = relationship(back_populates='property')
    address: Mapped[str] = mapped_column(String)
    area: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    total_floor: Mapped[int] = mapped_column(Integer)
    condition: Mapped[ConductionType] = mapped_column(Enum(ConductionType), nullable=True, default=ConductionType.среднее)
    documents: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    seller: Mapped[UserProfile] = relationship(back_populates='property')

    property_image: Mapped[List['PropertyImage']] = relationship(back_populates='property',
                                                                 cascade='all, delete-orphan')

    review: Mapped[List['Review']] = relationship(back_populates='property_review',
                                                  cascade='all, delete-orphan')



class PropertyImage(Base):
    __tablename__ = 'property_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    property: Mapped[Property] = relationship(back_populates='property_image')
    image: Mapped[str] = mapped_column(String)



class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    property_review: Mapped[Property] = relationship(back_populates='review')
    buyer_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    buyer: Mapped[UserProfile] = relationship(back_populates='buyer_review', foreign_keys=[buyer_id])
    owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    owner: Mapped[UserProfile] = relationship(back_populates='owner_review', foreign_keys=[owner_id])
    rating: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())



class HousePredict(Base):
    __tablename__ = 'predict'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    GrLivArea: Mapped[int] = mapped_column(Integer)
    YearBuilt: Mapped[int] = mapped_column(Integer)
    GarageCars: Mapped[int] = mapped_column(Integer)
    TotalBsmtSF: Mapped[int] = mapped_column(Integer)
    FullBath: Mapped[int] = mapped_column(Integer)
    OverallQual: Mapped[int] = mapped_column(Integer)
    Neighborhood: Mapped[str] = mapped_column(String)
    SalePrice: Mapped[float] = mapped_column(Float)