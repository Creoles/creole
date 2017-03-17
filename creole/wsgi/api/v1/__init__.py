# coding: utf-8
from flask import Blueprint
from flask_restful import Api

from .endpoint.user import UserInfoApi, CreateUserApi
from .endpoint.country import (
    CountryApi,
    AllCountryApi,
    CreateCountryApi,
    CityApi,
    CreateCityApi,
)
from .endpoint.shop import (
    ShopApi,
    CreateShopApi,
    ShopCompanyApi,
    ShopSearchApi,
    CreateShopCompanyApi,
)
from .endpoint.vehicle import (
    VehicleApi,
    CreateVehicleApi,
    VehicleCompanyApi,
    CreateVehicleCompanyApi,
)


blue_print = Blueprint('api_v1', __name__)
app = Api(blue_print)

# 用户
app.add_resource(UserInfoApi, '/user/<info>', endpoint='user-info')
app.add_resource(CreateUserApi, '/user/create_user', endpoint='user-create')

# 国家和城市
app.add_resource(CountryApi, '/country/<int:id>', endpoint='get-country')
app.add_resource(AllCountryApi, '/country/all', endpoint='get-all-country')
app.add_resource(CreateCountryApi, '/country/create', endpoint='create-country')
app.add_resource(CityApi, '/city/<int:id>', endpoint='get-city')
app.add_resource(CreateCityApi, '/city/create', endpoint='create-city')

# 购物店
app.add_resource(ShopApi, '/shop/<int:id>', endpoint='get-shop')
app.add_resource(ShopSearchApi, '/shop/search', endpoint='search-shop')
app.add_resource(CreateShopApi, '/shop/create_shop', endpoint='create-shop')
app.add_resource(ShopCompanyApi, '/shop_company/<int:id>', endpoint='get-shop-company')
app.add_resource(CreateShopCompanyApi, '/shop_company/create_company', endpoint='create-shop-company')

# 车辆
app.add_resource(VehicleApi, '/vehicle/<int:id>', endpoint='get-vehicle')
app.add_resource(CreateVehicleApi, '/vehicle/create_vehicle', endpoint='create-vehicle')
app.add_resource(VehicleCompanyApi, '/vehicle_company/<int:id>', endpoint='get-vehicle-company')
app.add_resource(CreateVehicleCompanyApi, '/vehicle_compnay/create_vehicle', endpoint='create-vehicle-company')
