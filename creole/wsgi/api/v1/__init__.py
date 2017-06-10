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
    CreateShopCompanyContactApi,
    ShopCompanyContactApi,
    GetShopCompanyContactApi,
    CreateShopFeeApi,
    ShopFeeApi,
    GetShopFeeApi,
    CreateShopContactApi,
    ShopContactApi,
    GetShopContactApi,
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
    GetVehicleFeeApi,
    VehicleFeeApi,
    CreateVehicleFeeApi,
    SearchVehicleFeeApi,
    VehicleContactApi,
    GetVehicleContactApi,
    CreateVehicleContactApi,
    VehicleTypeApi,
    CreateVehicleTypeApi,
    SearchVehicleTypeApi,
)
from .endpoint.attraction import (
    AttractionApi,
    CreateAttractionApi,
    SearchAttractionApi,
    CreateAttractionFeeApi,
    AttractionFeeApi,
    GetAttractionFeeApi,
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
from .endpoint.hotel import (
    HotelCompanyApi,
    CreateHotelCompanyApi,
    HotelCompanyContactApi,
    GetHotelCompanyContactApi,
    CreateHotelCompanyContactApi,
    HotelApi,
    CreateHotelApi,
    GetHotelApi,
    HotelAccountApi,
    CreateHotelAccountApi,
    GetHotelAccountApi,
    HotelContactApi,
    GetHotelContactApi,
    CreateHotelContactApi,
    CreateHotelFeeApi,
    HotelFeeApi,
    GetHotelFeeApi,
    EditRoomPriceApi,
    EditMealPriceApi,
    EditRoomAdditionalChargeApi,
    EditFestivalAdditionalChargeApi,
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
app.add_resource(CreateShopCompanyContactApi, '/shop/company/contact/create', endpoint='create-shop-company-contact')
app.add_resource(ShopCompanyContactApi, '/shop/company/contact/<int:id>', endpoint='get-shop-company-contact')
app.add_resource(GetShopCompanyContactApi, '/shop/company/contact/company/<int:company_id>', endpoint='get-shop-company-contact-by-company-id')
app.add_resource(CreateShopFeeApi, '/shop/fee/create', endpoint='create-shop-fee')
app.add_resource(ShopFeeApi, '/shop/fee/<int:id>', endpoint='get-shop-fee')
app.add_resource(GetShopFeeApi, '/shop/fee/shop/<int:shop_id>', endpoint='get-shop-fee-by-shop-id')
app.add_resource(CreateShopContactApi, '/shop/contact/create', endpoint='create-shop-contact')
app.add_resource(ShopContactApi, '/shop/contact/<int:id>', endpoint='get-shop-contact')
app.add_resource(GetShopContactApi, '/shop/contact/shop/<int:shop_id>', endpoint='get-shop-contact-by-shop-id')

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
app.add_resource(GetVehicleFeeApi, '/vehicle/fee/company/<int:company_id>', endpoint='get-company-vehicle-fee')
app.add_resource(CreateVehicleFeeApi, '/vehicle/fee/create', endpoint='create-vehicle-fee')
app.add_resource(SearchVehicleFeeApi, '/vehicle/fee/search', endpoint='search-vehicle-fee')
app.add_resource(VehicleContactApi, '/vehicle/contact/<int:id>', endpoint='get-vehicle-contact')
app.add_resource(GetVehicleContactApi, '/vehicle/contact/company/<int:company_id>', endpoint='get-company-contact')
app.add_resource(CreateVehicleContactApi, '/vehicle/contact/create', endpoint='create-vehicle-contact')
app.add_resource(VehicleTypeApi, '/vehicle/type/<int:id>', endpoint='get-vehicle-type')
app.add_resource(CreateVehicleTypeApi, '/vehicle/type/create', endpoint='create-vehicle-type')
app.add_resource(SearchVehicleTypeApi, '/vehicle/type/search', endpoint='search-vehicle-type')

# 景点
app.add_resource(AttractionApi, '/attraction/<int:id>', endpoint='get-attraction')
app.add_resource(CreateAttractionApi, '/attraction/create', endpoint='create-attraction')
app.add_resource(SearchAttractionApi, '/attraction/search', endpoint='search-attraction')
app.add_resource(CreateAttractionFeeApi, '/attraction/fee/create', endpoint='create-attraction-fee')
app.add_resource(AttractionFeeApi, '/attraction/fee/<int:id>', endpoint='get-attraction-fee')
app.add_resource(GetAttractionFeeApi, '/attraction/fee/attraction/<int:attraction_id>', endpoint='get-fee')

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

# 酒店
app.add_resource(HotelApi, '/hotel/<int:id>', endpoint='get-hotel')
app.add_resource(CreateHotelApi, '/hotel/create', endpoint='create-hotel')
app.add_resource(GetHotelApi, '/hotel/get/<int:company>', endpoint='get-hotel-by-company')
app.add_resource(CreateHotelFeeApi, '/hotel/fee/create', endpoint='create-hotel-fee')
app.add_resource(HotelFeeApi, '/hotel/fee/<int:id>', endpoint='get-hotel-fee')
app.add_resource(GetHotelFeeApi, '/hotel/fee/hotel/<int:hotel_id>', endpoint='get-hotel-fee-by-hotel-id')
app.add_resource(EditRoomPriceApi, '/hotel/room_price/edit', endpoint='edit-room-price')
app.add_resource(EditMealPriceApi, '/hotel/meal_price/edit', endpoint='edit-meal-price')
app.add_resource(EditRoomAdditionalChargeApi, '/hotel/room_additional_charge', endpoint='edit-room-additional-charge')
app.add_resource(EditFestivalAdditionalChargeApi, '/hotel/festival_additional_charge/edit', endpoint='edit-festival-additional-charge')
app.add_resource(HotelCompanyApi, '/hotel/company/<int:id>', endpoint='get-hotel-company')
app.add_resource(CreateHotelCompanyApi, '/hotel/company/create', endpoint='create-hotel-company')
app.add_resource(HotelCompanyContactApi, '/hotel/company/contact/<int:id>', endpoint='get-hotel-company-contact')
app.add_resource(GetHotelCompanyContactApi, '/hotel/company/contact/company/<int:company_id>', endpoint='get-hotel-company-contact-by-company-id')
app.add_resource(CreateHotelCompanyContactApi, '/hotel/company/contact/create', endpoint='create-hotel-company-contact')
app.add_resource(HotelContactApi, '/hotel/contact/<int:id>', endpoint='get-hotel-contact')
app.add_resource(GetHotelContactApi, '/hotel/contact/hotel/<int:hotel_id>', endpoint='get-hotel-contact-by-hotel-id')
app.add_resource(CreateHotelContactApi, '/hotel/contact/create', endpoint='create-hotel-contact')
app.add_resource(HotelAccountApi, '/hotel/account/<int:id>', endpoint='get-hotel-account')
app.add_resource(CreateHotelAccountApi, '/hotel/account/create', endpoint='create-hotel-account')
app.add_resource(GetHotelAccountApi, '/hotel/account/hotel/<int:hotel_id>', endpoint='get-hotel-account-by-hotel-id')
