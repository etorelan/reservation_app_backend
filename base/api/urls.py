from django.urls import path
from .views import *

urlpatterns = [
    path("products/", get_hotel_view, name="get_hotel_view"),
    path("images/<str:image>", get_images_view, name="get_images_view"),
    path("images/hotel/<int:id>", get_single_product_page_images, name="get_single_product_page_images"),
    path("search-bar/<search_input>", get_search_bar_options, name="get_search_bar_options"),
    path("hotel-rooms/", find_all_room_types, name="find_rooms"),
    path("availability/",find_available_room, name="find_available_room"),
    path("pend-reserve/", ensure_one_reservation_per_guest, name="ensure_one_reservation_per_guest"),
    path("reservation-info/", get_reservation_info, name="get_reservation_info"),
    path("reserve/", reserve, name="reserve"),
    path("is-allowed/", is_user_allowed, name="is_user_allowed"),
    path("cancel-reservation/", cancel_reservation, name="cancel_reservation"),
    path("create-checkout-session/", create_checkout_session),
]