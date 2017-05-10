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
    SearchShopCompanyApi,
)
from .endpoint.vehicle import (
    VehicleApi,
    SearchVehicleApi,
    CreateVehicleApi,
    VehicleCompanyApi,
    CreateVehicleCompanyApi,
    SearchVehicleCompanyApi,
    VehicleAccountApi,
    CreateVehicleAccountApi,
    VehicleFeeApi,
    CreateVehicleFeeApi,
    VehicleContactApi,
    CreateVehicleContactApi,
    VehicleTypeApi,
    CreateVehicleTypeApi,
)
from .endpoint.attraction import (
    AttractionApi,
    CreateAttractionApi,
    SearchAttractionApi,
)
from .endpoint.restaurant import (
    RestaurantApi,
    CreateRestaurantApi,
    SearchRestaurantApi,
    EditRestaurantAccountApi,
    RestaurantAccountApi,
    MealApi,
    EditMealApi,
)
from .endpoint.tour_guide import (
    TourGuideApi,
    SearchTourGuideApi,
    CreateTourGuideApi,
    TourGuideFeeApi,
    CreateTourGuideFeeApi,
    TourGuideAccountApi,
    EditTourGuideAccountApi,
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
app.add_resource(CreateShopApi, '/shop/create', endpoint='create-shop')
app.add_resource(ShopCompanyApi, '/shop/company/<int:id>', endpoint='get-shop-company')
app.add_resource(CreateShopCompanyApi, '/shop/company/create', endpoint='create-shop-company')
app.add_resource(SearchShopCompanyApi, '/shop/company/search', endpoint='search-shop-company')

# 车辆
app.add_resource(VehicleApi, '/vehicle/<int:id>', endpoint='get-vehicle')
app.add_resource(CreateVehicleApi, '/vehicle/create', endpoint='create-vehicle')
app.add_resource(SearchVehicleApi, '/vehicle/search', endpoint='search-vehicle')
app.add_resource(VehicleCompanyApi, '/vehicle/company/<int:id>', endpoint='get-vehicle-company')
app.add_resource(CreateVehicleCompanyApi, '/vehicle/company/create', endpoint='create-vehicle-company')
app.add_resource(SearchVehicleCompanyApi, '/vehicle/company/search', endpoint='search-vehicle-company')
app.add_resource(VehicleAccountApi, '/vehicle/account/<int:id>', endpoint='get-vehicle-account')
app.add_resource(CreateVehicleAccountApi, '/vehicle/account/create', endpoint='create-account')
app.add_resource(VehicleFeeApi, '/vehicle/fee/<int:id>', endpoint='get-vehicle-fee')
app.add_resource(CreateVehicleFeeApi, '/vehicle/fee/create', endpoint='create-vehicle-fee')
app.add_resource(VehicleContactApi, '/vehicle/contact/<int:id>', endpoint='get-vehicle-contact')
app.add_resource(CreateVehicleContactApi, '/vehicle/contact/create', endpoint='create-vehicle-contact')
app.add_resource(VehicleTypeApi, '/vehicle/type/<int:id>', endpoint='get-vehicle-type')
app.add_resource(CreateVehicleTypeApi, '/vehicle/type/create', endpoint='create-vehicle-type')

# 景点
app.add_resource(AttractionApi, '/attraction/<int:id>', endpoint='get-attraction')
app.add_resource(CreateAttractionApi, '/attraction/create', endpoint='create-attraction')
app.add_resource(SearchAttractionApi, '/attraction/search', endpoint='search-attraction')

# 餐饮
app.add_resource(RestaurantApi, '/restaurant/<int:id>', endpoint='get-restaurant')
app.add_resource(CreateRestaurantApi, '/restaurant/create', endpoint='create-restaurant')
app.add_resource(SearchRestaurantApi, '/restaurant/search', endpoint='search-restaurant')
app.add_resource(RestaurantAccountApi, '/restaurant/account/<int:restaurant_id>', endpoint='get-restaurant-account')
app.add_resource(EditRestaurantAccountApi, '/restaurant/account/edit', endpoint='edit-restaurant-account')
app.add_resource(MealApi, '/restaurant/meal/<int:restaurant_id>', endpoint='get-restaurant-meal')
app.add_resource(EditMealApi, '/restaurant/meal/edit', endpoint='edit-restaurant-meal')

# 导游
app.add_resource(TourGuideApi, '/tour_guide/<int:id>', endpoint='get-tour-guide')
app.add_resource(SearchTourGuideApi, '/tour_guide/search', endpoint='search-tour-guide')
app.add_resource(CreateTourGuideApi, '/tour_guide/create', endpoint='create-tour-guide')
app.add_resource(TourGuideFeeApi, '/tour_guide/fee/<int:id>', endpoint='get-tour-guide-fee')
app.add_resource(CreateTourGuideFeeApi, '/tour_guide/fee/create', endpoint='create-tour-guide-fee')
app.add_resource(TourGuideAccountApi, '/tour_guide/account/<int:tour_guide_id>', endpoint='get-tour-guide-account')
app.add_resource(EditTourGuideAccountApi, '/tour_guide/account/edit', endpoint='edit-tour-guide-account')
