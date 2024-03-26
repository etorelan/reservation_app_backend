from datetime import timedelta, datetime
import os, dotenv, json, math, stripe

from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models import *
from .serializers import HotelSerializer, create_serializer
from .helpful_functions import makeDateAware, isOverlapping, start_before_end

from django.http import HttpResponse


##################### DJANGO PAGINATION ##############
NUM_OF_HOTELS_PER_PAGE = 24

#################### STRIPE SETUP ####################
dotenv.load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")


DOMAIN = "http://localhost:3000"


@api_view(["POST"])
def create_checkout_session(request):
    body = json.loads(request.body)
    reservation_id = int(body["reservationID"])
    stripe_id = Reservation.objects.get(
        pk=reservation_id
    ).room.room_type.stripe_price_id
    print(body)

    domain_append = f"&reservationID={reservation_id}&firstName={body['firstName']}&lastName={body['lastName']}&phoneNumber={body['phoneNumber']}&country={body['country']['label']}"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": stripe_id,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=DOMAIN + f"?success=true{domain_append}",
            cancel_url=DOMAIN + f"?canceled=true{domain_append}",
        )
    except Exception as e:
        print("📛 ", str(e))
        return HttpResponse(str(e), status=500)

    return Response({"url": checkout_session.url})


@api_view(["GET"])
def get_hotel_view(request):

    key_filters = {key: None for key in ["country", "city", "category", "star_rating"]}
    key_filters["page"] = 1

    other_filters = []

    for key, value in request.GET.items():
        value = json.loads(value)
        if key == "star_rating" and value and type(value) == list:
            key_filters["star_rating"] = Q(star_rating=value[0])
            for star in value[1:]:
                key_filters["star_rating"] = key_filters["star_rating"] | Q(
                    star_rating=star
                )

        elif key in ["country", "city", "category", "page"]:
            key_filters[key] = value
        else:
            other_filters.append({key: value})

    print(f"✅ Request filters {key_filters}")

    PAGE_START = (key_filters["page"] - 1) * NUM_OF_HOTELS_PER_PAGE
    PAGE_END = PAGE_START + NUM_OF_HOTELS_PER_PAGE

    hotel_serializer_class, hotel_serializer = HotelSerializer, None
    num_hotels = 1

    if not key_filters["country"]:
        hotels = Hotel.objects.all()
        print("✅ First boot")
    else:
        try:
            country = Country.objects.get(name=key_filters["country"])  # country --->
        except Country.DoesNotExist:
            print("📛 get_hotel_view: Country not found")
            raise ValueError("📛 get_hotel_view: Country not found")

        if key_filters["city"]:
            try:
                city = country.country_cities.get(name=key_filters["city"])
            except City.DoesNotExist:
                raise ValueError("📛 get_hotel_view: City not found")

            hotels = city.city_hotels.all()

            if key_filters["category"] != None:
                hotels = hotels.filter(category_id=key_filters["category"])
                print("✅ Path: country ---> city ---> category")
            else:
                print("✅ Path: country ---> city")

        elif key_filters["category"] != None:
            try:
                category = Category.objects.get(pk=key_filters["category"])
            except Category.DoesNotExist:
                raise ValueError("📛 get_hotel_view: Category not found")

            hotels = category.category_hotels.filter(
                city__country__name=key_filters["country"]
            )
            print("✅ Path: country + category")

        else:
            hotels = Hotel.objects.filter(city__country__name=key_filters["country"])
            print("✅ Path: country ")

        if key_filters["star_rating"]:
            hotels = hotels.filter(key_filters["star_rating"])

        for f in other_filters:
            hotels = hotels.filter(**f)

    num_hotels = hotels.count()
    hotels = hotels[PAGE_START:PAGE_END]
    hotel_serializer = hotel_serializer_class(hotels, many=True)
    print("✅ Showing ", len(hotel_serializer.data), " hotels")

    return Response(
        {
            "hotels_info": hotel_serializer.data,
            "count_of_pages_to_show": math.ceil(num_hotels / NUM_OF_HOTELS_PER_PAGE),
        }
    )


@api_view(["GET"])
def get_images_view(request, image):
    return FileResponse(open(f"media/images/{image}", "rb"), content_type="image/webp")


@api_view(["GET"])
def get_search_bar_options(request, search_input):
    # The function favors searching countries first, and only if unsuccessful in matching
    # the query does the function move to querying the city model, as it is larger and
    # thus more computationally expensive

    parsed_input = json.loads(search_input)
    query, country_name = parsed_input["query"], parsed_input["countryName"]

    def create_cities_response(cities):
        city_data = []
        for city in cities:
            city_data.append({"city": city.name, "country_name": city.country.name})
        return Response(city_data)

    if country_name:
        try:
            country = Country.objects.get(name=country_name)
        except Country.DoesNotExist:
            raise ValueError("⚠️  get_search_bar_options: Country not found")

        cities = country.country_cities.filter(name__icontains=query)[:5]
        return create_cities_response(cities)
    countries = Country.objects.filter(name__icontains=query)[:5]
    if countries.exists():
        return Response([country.name for country in countries])

    cities = City.objects.filter(name__icontains=query)[:5]
    return create_cities_response(cities)


@api_view(["GET"])
def get_single_product_page_images(request, id):
    try:
        hotel = Hotel.objects.get(pk=id)
    except Hotel.DoesNotExist:
        raise ValueError("📛 get_single_product_page_images: Hotel not found")

    images = hotel.hotel_images.all()

    hotel_serializer = HotelSerializer(hotel)
    response = [hotel_serializer.data]

    for element in images:
        response.append(str(element.image))

    return Response(response)


@api_view(["POST"])
def find_all_room_types(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    hotel_id = body.get("hotel")
    if not hotel_id:
        return Response(
            {"error": "Missing 'hotel' parameter"}, status=status.HTTP_400_BAD_REQUEST
        )

    hotel = get_object_or_404(Hotel, pk=hotel_id)

    room_types = hotel.hotel_room_types.all()
    response = []
    for room_type in room_types:
        response.append(
            {
                "type": room_type.name,
                "description": room_type.description,
                "price": room_type.current_price,
            }
        )
    print(response)

    return Response(response)


@api_view(["POST"])
def find_available_room(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    guest = None
    try:
        guest = Guest.objects.get(email=body["email"])
    except Guest.DoesNotExist:
        pass

    hotel_id = body.get("hotelId")
    if not hotel_id:
        return Response(
            {"error": "Missing hotel id"}, status=status.HTTP_400_BAD_REQUEST
        )
    hotel = Hotel.objects.get(pk=hotel_id)

    start_date, end_date = makeDateAware(date=body["startDate"]), makeDateAware(
        date=body["endDate"]
    )

    res = start_before_end(start_date=start_date, end_date=end_date)
    if res:
        return res

    room_types = hotel.hotel_room_types.all()
    response = {rt.name: [] for rt in list(room_types)}

    for room_type in room_types:
        for room in room_type.room_type_rooms.all():

            overlaps = isOverlapping(
                room=room, start_date=start_date, end_date=end_date, guest=guest
            )
            if not overlaps:
                response[room_type.name].append(room.pk)

    print(response)
    return Response(response)


@api_view(["POST"])
def ensure_one_reservation_per_guest(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    if "email" not in body:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    hotel = get_object_or_404(Hotel, pk=body["hotelId"])
    room_type = get_object_or_404(hotel.hotel_room_types, name=body["roomType"])
    room = get_object_or_404(room_type.room_type_rooms, pk=body["roomId"])

    print("Requested room ID: ", room.id)

    start_date, end_date = makeDateAware(date=body["startDate"]), makeDateAware(
        date=body["endDate"]
    )

    res = start_before_end(start_date=start_date, end_date=end_date)
    if res:
        return res

    price = room_type.current_price

    try:
        guest = Guest.objects.get(email=body["email"])
        overlaps = isOverlapping(
            room=room, start_date=start_date, end_date=end_date, guest=guest
        )
        if overlaps:
            # Room already reserved during request
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

        reservation = guest.guest_reservations.filter(
            room__room_type__name=body["roomType"], status="PEND"
        )
        print("Guest's pending reservations count: ", reservation)

        if len(reservation) > 1:
            raise ValueError(
                f"📛 ensure_one_reservation_per_guest: {guest.email} has more than 1 reservation"
            )

        if len(reservation):
            return Response(list(reservation)[0].id)

        reservation = Reservation.objects.create(
            guest=guest,
            room=room,
            check_in_date_time=start_date,
            check_out_date_time=end_date,
            total_price=price,
        )
        return Response(reservation.id)

    except Guest.DoesNotExist:
        print("📛 ensure_one_reservation_per_guest: Guest not found")
        return Response(
            {"error": "Guest DoesNotExist"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def get_reservation_info(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    reservation = get_object_or_404(Reservation , pk=int(body["reservationID"]))
    if reservation.status != "PEND":
        return Response(
        {"error": "Reservation not pending"}, status=status.HTTP_400_BAD_REQUEST
    )

    # A celery worker deletes all PEND transaction older than 20 minutes
    # the 18 minute buffer ensures the timely completion of the task 
    if reservation.time_created + timedelta(minutes=18) < timezone.now():
        return Response(
        {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
    )
    print(reservation.id)

    serializer_class = create_serializer(Reservation)
    serializer = serializer_class(reservation)
    return Response(serializer.data)



@api_view(["POST"])
def is_user_allowed(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        get_object_or_404(Reservation, pk=int(body["reservationID"]), guest__email=body["email"], status="PEND")
        return Response(status=status.HTTP_200_OK)
    except Http404:
        print("📛 is_user_allowed: Reservation not found")
        return Response(status=403, exception=True)


@api_view(["DELETE"])
def cancel_reservation(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    reservation = get_object_or_404(Reservation , pk=int(body.get("reservationID")))
    if reservation.guest.email == body["email"]:
        reservation.delete()
    else:
        return Response(status=status.HTTP_409_CONFLICT, exception=True)
    return Response()


@api_view(["PATCH"])
def reserve(request):
    body = {}
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
        )

    # {'success': 'true', 'reservation_id': '46', 'firstName': 'a', 'lastName': 'Jezty', 'phoneNumber': '949133955', 'country': 'United Arab Emirates'}

    # update reservation status
    try:
        invoice = InvoiceGuest.objects.get(reservation=int(body.get("reservationID")))
        print(f"📛 Reservation: Invoice {invoice.id} already created")
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except InvoiceGuest.DoesNotExist:

        # reservation = Reservation.objects.get(pk=int(body.get("reservationID")))
        reservation = get_object_or_404(Reservation,pk=int(body.get("reservationID")))
        reservation.status = "CNFR"
        reservation.save()

        # state = Country.objects.get(name=body["country"])
        state = get_object_or_404(Country, name=body["country"])
        if not state:
            newCountry = Country.objects.create(name=body["country"])
            newCountry.save()
            state = newCountry

        guest = Guest.objects.get(pk=reservation.guest.email)
        if len(guest.first_name) == 0:
            guest.country = state
            guest.first_name = body["firstName"]
            guest.last_name = body["lastName"]
            guest.phone = body["phoneNumber"]
            guest.save()

        invoice = InvoiceGuest.objects.create(
            guest=guest, reservation=reservation, invoice_amount=reservation.total_price
        )
        print(
            f"Invoice {invoice.id} for {guest.last_name} of {invoice.invoice_amount} has been created"
        )
        return Response()
