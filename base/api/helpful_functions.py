import stripe, os

from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response

from base.models import Hotel, RoomType
from base.tests.helpful_test_functions import now_aware


stripe.api_key = os.getenv("STRIPE_API_KEY")


def makeDateAware(date):
    res = datetime.strptime(date, "%Y-%m-%d")
    res = timezone.make_aware(res, timezone.get_default_timezone())
    return res


def isOverlapping(room, start_date, end_date, guest=None) -> bool:
    overlapping_query = Q(
        room=room, check_in_date_time__lte=end_date, check_out_date_time__gte=start_date
    )

    if guest:
        overlapping_query &= ~Q(guest=guest)

    overlapping = room.room_reservations.filter(overlapping_query)
    return overlapping.exists()


def start_before_end(start_date, end_date):
    if end_date - start_date <= timedelta(hours=23, minutes=59):
        return Response(
            {"error": "start date is higher than end date"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if start_date.date() < now_aware().date() or end_date.date() < now_aware().date():
        return Response(
            {"error": "start date is in the past"}, status=status.HTTP_400_BAD_REQUEST
        )
    return None


def create_stripe_product(hotel_ID, room_type_ID):
    hotel_name = Hotel.objects.get(pk=hotel_ID).name
    room_type = RoomType.objects.get(pk=room_type_ID)

    name, description, price = (
        room_type.name,
        room_type.description,
        room_type.current_price,
    )

    product = stripe.Product.create(
        name=name, description=hotel_name + " " + description
    )
    return product, price


def create_stripe_price(product_ID, amount, currency="EUR"):
    price = stripe.Price.create(
        product=product_ID,
        unit_amount=int(amount * 100),  # price is set in cents
        currency=currency,
    )
    return price
