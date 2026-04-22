from pydantic import BaseModel, EmailStr
from .models import RoleChoices, PropertyType, ConductionType
from datetime import date,datetime
from typing import Optional



class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    avatar: Optional[str]
    role: RoleChoices
    data_register: date



class UserProfileListSchema(BaseModel):
    id: int
    username: str
    avatar: Optional[str]
    role: RoleChoices


class UserLoginSchema(BaseModel):
    login: str
    password: str



class UserProfileInputSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    avatar: Optional[str]
    role: RoleChoices



class RegionOutSchema(BaseModel):
    id: int
    region_name: str


class RegionInputSchema(BaseModel):
    region_name: str


class CityOutSchema(BaseModel):
    id: int
    city_name: str
    region_id: int


class CityInputSchema(BaseModel):
    city_name: str
    region_id: int


class DistrictOutSchema(BaseModel):
    id: int
    city_id: int
    district_name: str


class DistrictInputSchema(BaseModel):
    city_id: int
    district_name: str


class PropertyOutSchema(BaseModel):
    id: int
    title: str
    description: str
    property_type: PropertyType
    region_id: int
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floor: int
    condition: ConductionType
    documents: bool
    seller_id: int



class PropertyInputSchema(BaseModel):
    title: str
    description: str
    property_type: PropertyType
    region_id: int
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floor: int
    condition: ConductionType
    documents: bool
    seller_id: int


class PropertyImageOutSchema(BaseModel):
    id: int
    property_id: int
    image: str


class PropertyImageInputSchema(BaseModel):
    property_id: int
    image: str


class ReviewOutSchema(BaseModel):
    id: int
    property_id: int
    buyer_id: int
    owner_id: int
    rating: int
    comment: str
    created_date: datetime


class ReviewInputSchema(BaseModel):
    property_id: int
    buyer_id: int
    owner_id: int
    rating: int
    comment: str


class HousePredictSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str