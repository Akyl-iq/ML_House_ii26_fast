from .views import (UserProfileAdmin, CityAdmin, RegionAdmin, DistrictAdmin,  PropertyAdmin, RefreshTokenAdmin,
                    PropertyImageAdmin, ReviewAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from my_project.database.db import engine



def setup_admin(my_project: FastAPI):
    admin = Admin(my_project, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(PropertyImageAdmin)