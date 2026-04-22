from my_project.database.models import (UserProfile, Region, City,District,Review, RefreshToken, Property, PropertyImage)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model= UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CityAdmin(ModelView, model= City):
    column_list = [City.city_name]


class RefreshTokenAdmin(ModelView, model= RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.token]


class DistrictAdmin(ModelView, model= District):
    column_list = [District.district_name]


class RegionAdmin(ModelView, model= Region):
    column_list = [Region.region_name]


class PropertyAdmin(ModelView, model= Property):
    column_list = [Property.title]


class PropertyImageAdmin(ModelView, model= PropertyImage):
    column_list = [PropertyImage.id, PropertyImage.image]


class ReviewAdmin(ModelView, model= Review):
    column_list = [Review.comment]