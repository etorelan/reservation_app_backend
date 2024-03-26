from django.db import transaction
from datetime import datetime, timedelta
from django.utils import timezone


from base.models import *


def define_reservation_comps(start=None, end=None, room_id=1, email="estate@email.com"):
    with transaction.atomic():
        room = Room.objects.get(pk=room_id)
        guest = Guest.objects.get(email=email)
        start_date = timezone.now() + timedelta(hours=4) if not start else start
        end_date = start_date + timedelta(hours=50) if not end else end

        reservation = define_new_reservation(
            guest=guest, room=room, check_in=start_date, check_out=end_date
        )
        reservation.save()
    return (room, guest, start_date, end_date, reservation)


def now_aware():
    return timezone.make_aware(datetime.now(), timezone.get_current_timezone())


def define_new_hotel(
    self,
    star_rating=4,
    service=3,
    review_count=10,
    review_rating=8.5,
    name="Test Hotel",
) -> Hotel:
    return Hotel(
        name=name,
        city=self.city,
        category=self.category,
        star_rating=star_rating,
        service=service,
        review_count=review_count,
        review_rating=review_rating,
    )


def define_new_room_type(
    self=None,
    hotel=None,
    name="Standard Room",
    description="A standard room description",
    current_price=Decimal("99.99"),
    stripe_price_id="price_123",
) -> RoomType:
    return RoomType(
        hotel=self.hotel if not hotel else hotel,
        name=name,
        description=description,
        current_price=current_price,
        stripe_price_id=stripe_price_id,
    )


def define_new_guest(
    self=None,
    country=None,
    email="test@example.com",
    first_name="John",
    last_name="Doe",
    phone="1234567890",
) -> Guest:
    return Guest(
        email=email,
        country=self.country if not country else country,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )


def define_new_reservation(
    self=None,
    guest=None,
    room=None,
    check_in=timezone.now(),
    check_out=timezone.now(),
    total_price=Decimal("99.99"),
    status=None,
):

    res = Reservation(
        guest=self.guest if not guest else guest,
        room=self.room if not room else room,
        check_in_date_time=check_in,
        check_out_date_time=check_out,
        total_price=total_price,
    )
    if status:
        res.status = status
    return res


def reservation_invoice_setup(cls):
    with transaction.atomic():
        setup_test_data(cls=cls)
        cls.guest = define_new_guest(country=cls.country)
        cls.room_type = define_new_room_type(hotel=cls.hotel)
        cls.guest.save()
        cls.room_type.save()
        cls.room = Room.objects.create(name="Test Room", room_type=cls.room_type)


def create_model_testcase(
    self,
    test_case_array,
    model_field,
    curr_instance,
    new_instance_func,
    error=ValidationError,
):
    # change the args to be better
    for test_case in test_case_array:
        with self.assertRaises(error):
            with transaction.atomic():
                if "price" in model_field:
                    test_case = Decimal(str(test_case))
                inst = new_instance_func(self, **{model_field: test_case})
                inst.full_clean()

    for test_case in test_case_array:
        with self.assertRaises(error):
            with transaction.atomic():
                setattr(curr_instance, model_field, test_case)
                curr_instance.full_clean()


def setup_test_data(cls):
    with transaction.atomic():
        cls.country = Country.objects.create(name="United States")
        cls.city = City.objects.create(name="Test City", country=cls.country)
        cls.category = Category.objects.create(name="Test Category")
        cls.hotel = Hotel.objects.create(
            name="Test Hotel",
            city=cls.city,
            category=cls.category,
            star_rating=4,
            service=3,
            review_count=10,
            review_rating=8.5,
        )
