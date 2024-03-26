import json, math

from django.test import TestCase

from django.urls import reverse
from django.db.models import Q
from django.test import Client

from datetime import timedelta

from urllib.parse import urlencode, quote

# from rest_framework.test import APIClient
from .helpful_test_functions import *

from base.models import *
from base.api.views import NUM_OF_HOTELS_PER_PAGE
from base.api.helpful_functions import isOverlapping


def isCorrectResponse(self, url, expected_response):
    response = self.client.get(url)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, expected_response)


class GetHotelViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def quoted_assert_many(self, query_params, expected):
        query_string = "&".join(
            [f"{key}={quote(str(value))}" for key, value in query_params.items()]
        )
        url = reverse("get_hotel_view") + "?" + query_string
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for res_h, exp_h in zip(response.data["hotels_info"], expected):
            self.assertEqual(res_h["id"], exp_h.id)

    def test_star_rating(self):
        query_params = {
            "country": '"Turkey"',
            "star_rating": "[2,3,4,5]",
        }

        ratings = [2, 3, 4, 5]
        star_rating = Q(star_rating=ratings[0])
        for star in ratings[1:]:
            star_rating = star_rating | Q(star_rating=star)

        hotels = Hotel.objects.filter(city__country__name="Turkey")

        expected_hotels = hotels.filter(star_rating)

        self.quoted_assert_many(query_params=query_params, expected=expected_hotels)

    def test_star_rating_is_array(self):
        query_params = {
            "star_rating": "2,3,4,5",
        }
        query_string = urlencode(query_params)
        url = reverse("get_hotel_view") + "?" + query_string

        with self.assertRaises(json.decoder.JSONDecodeError):
            response = self.client.get(url)

    def test_no_country(self):
        query_params = {
            "star_rating": "[2,3,4,5]",
        }
        query_string = urlencode(query_params)
        url = reverse("get_hotel_view") + "?" + query_string

        expected_hotel_info = Hotel.objects.all()[:NUM_OF_HOTELS_PER_PAGE]
        expect_page_count = math.ceil(Hotel.objects.count() / NUM_OF_HOTELS_PER_PAGE)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["hotels_info"]), NUM_OF_HOTELS_PER_PAGE)
        self.assertEqual(response.data["count_of_pages_to_show"], expect_page_count)

        for res_h, exp_h in zip(response.data["hotels_info"], expected_hotel_info):
            self.assertEqual(res_h["id"], exp_h.id)

    def test_country_incorrect(self):
        query_params = {
            "country": '"Tur"',
        }

        query_string = "&".join(
            [f"{key}={quote(str(value))}" for key, value in query_params.items()]
        )
        url = reverse("get_hotel_view") + "?" + query_string

        with self.assertRaises(ValueError):
            self.client.get(url)

    def test_country_city(self):
        query_params = {"country": '"Turkey"', "city": '"Antakya"'}

        country = Country.objects.get(name="Turkey")
        city = country.country_cities.get(name="Antakya")
        expected_hotels = city.city_hotels.all()[:NUM_OF_HOTELS_PER_PAGE]

        self.quoted_assert_many(query_params=query_params, expected=expected_hotels)

    def test_city_incorrect(self):
        query_params = {"country": '"Turkey"', "city": '"An"'}
        query_string = "&".join(
            [f"{key}={quote(str(value))}" for key, value in query_params.items()]
        )
        url = reverse("get_hotel_view") + "?" + query_string

        with self.assertRaises(ValueError):
            self.client.get(url)

    def test_country_city_category(self):
        query_params = {"country": '"Turkey"', "city": '"Antakya"', "category": 0}

        country = Country.objects.get(name="Turkey")
        city = country.country_cities.get(name="Antakya")
        all_city = city.city_hotels.all()
        expected_hotels = all_city.filter(category_id=0)

        self.quoted_assert_many(query_params=query_params, expected=expected_hotels)

    def test_country_city_category_incorrect(self):
        query_params = {"country": '"Turkey"', "city": '"Antakya"', "category": 100000}

        query_string = "&".join(
            [f"{key}={quote(str(value))}" for key, value in query_params.items()]
        )
        url = reverse("get_hotel_view") + "?" + query_string

        isCorrectResponse(
            self=self,
            url=url,
            expected_response={"hotels_info": [], "count_of_pages_to_show": 0},
        )

    def test_country_category(self):
        query_params = {"country": '"Turkey"', "category": 0}

        category = Category.objects.get(pk=0)
        expected_hotels = category.category_hotels.filter(city__country__name="Turkey")

        self.quoted_assert_many(query_params=query_params, expected=expected_hotels)

    def test_country_category_incorrect(self):
        query_params = {"country": '"Turkey"', "category": 100000}

        query_string = "&".join(
            [f"{key}={quote(str(value))}" for key, value in query_params.items()]
        )
        url = reverse("get_hotel_view") + "?" + query_string
        with self.assertRaises(ValueError):
            self.client.get(url)


class GetImagesViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_get_images_view(self):
        image_filename = "test_image.webp"

        url = reverse("get_images_view", args=[image_filename])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "image/webp")
        self.assertTrue(response.streaming_content)
        with open(f"media/images/{image_filename}", "rb") as image_file:
            expected_content = image_file.read()
        self.assertEqual(b"".join(response.streaming_content), expected_content)


class GetSearchBarOptionsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_without_country(self):
        search_inputs = [
            {"query": "Unit", "countryName": ""},
            {"query": "qz", "countryName": ""},
        ]
        for i, search_input in enumerate(search_inputs):
            search_input = json.dumps(search_input)
            expected_response = (
                ["United Arab Emirates", "United Kingdom", "United States"]
                if not i
                else []
            )

            url = reverse("get_search_bar_options", args=[search_input])
            isCorrectResponse(self=self, url=url, expected_response=expected_response)

    def test_will_default_city(self):
        search_input = {"query": "Ash", "countryName": ""}
        search_input = json.dumps(search_input)
        expected_response = [
            {"city": "Ashgabat", "country_name": "Turkmenistan"},
            {"city": "Ashkāsham", "country_name": "Afghanistan"},
            {"city": "Bashkia Vlorë", "country_name": "Albania"},
            {"city": "Bashkia Shijak", "country_name": "Albania"},
            {"city": "Bashkia Kurbin", "country_name": "Albania"},
        ]

        url = reverse("get_search_bar_options", args=[search_input])
        isCorrectResponse(self=self, url=url, expected_response=expected_response)

    def test_with_country(self):
        search_inputs = [
            {"query": "A", "countryName": "Turkmenistan"},
            {"query": "A", "countryName": "Turkmeni"},
        ]
        for i, search_input in enumerate(search_inputs):
            search_input = json.dumps(search_input)
            expected_response = (
                [
                    {"city": "Ashgabat", "country_name": "Turkmenistan"},
                    {"city": "Atamyrat", "country_name": "Turkmenistan"},
                    {"city": "Boldumsaz", "country_name": "Turkmenistan"},
                    {"city": "Bayramaly", "country_name": "Turkmenistan"},
                    {"city": "Baharly", "country_name": "Turkmenistan"},
                ]
                if not i
                else {"error": "Country not found"}
            )

            url = reverse("get_search_bar_options", args=[search_input])
            if not i:
                isCorrectResponse(
                    self=self, url=url, expected_response=expected_response
                )
            else:
                with self.assertRaises(ValueError):
                    self.client.get(url)


class GetSingleProductPageImagesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_hotel_incorrect(self):
        hotel_id = 10 ** 9
        url = reverse("get_single_product_page_images", args=[hotel_id])
        with self.assertRaises(ValueError):
            self.client.get(url)

    def test_returns_images(self):
        hotel_id = 1
        hotel = Hotel.objects.get(pk=hotel_id)

        url = reverse("get_single_product_page_images", args=[hotel_id])
        images = hotel.hotel_images.all()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for img, res in zip(images, response.data[1:]):
            self.assertEqual(img.image, res)


class FindAllRoomTypesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_correct_return_json_format(self):
        data = {
            "hotel": 1,
        }

        url = reverse("find_rooms")
        response = self.client.generic("POST", url, data=json.dumps(data))

        expected_keys = ["type", "description", "price"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), list)
        self.assertGreater(len(response.data), 0)

        arr = response.data
        for key in expected_keys:
            for elem in arr:
                self.assertIn(key, elem)

        elem = arr[0]
        self.assertEqual(type(elem["type"]), str)
        self.assertEqual(type(elem["type"]), str)
        self.assertEqual(type(elem["price"]), Decimal)

    def test_correct_response(self):
        data = {
            "hotel": 1,
        }

        url = reverse("find_rooms")
        response = self.client.generic("POST", url, data=json.dumps(data))

        expected = []
        hotel = Hotel.objects.get(pk=1)
        room_types = hotel.hotel_room_types.all()
        for room_type in room_types:
            expected.append(
                {
                    "type": room_type.name,
                    "description": room_type.description,
                    "price": room_type.current_price,
                }
            )
        self.assertEqual(response.data, expected)

    def test_invalid_json(self):
        data = "{'hotel': 1,"
        url = reverse("find_rooms")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_hotel(self):
        data = {}
        url = reverse("find_rooms")
        response = self.client.generic("POST", url, data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_nonexistant_hotel_id(self):
        data = {"hotel": -1}
        url = reverse("find_rooms")
        response = self.client.generic("POST", url, data=json.dumps(data))
        self.assertEqual(response.status_code, 404)


class FindAvailableRoomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("find_available_room")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_hotel_id(self):
        data = {"email": 1}
        url = reverse("find_available_room")
        response = self.client.generic("POST", url, data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_find_available_room(self):
        startDate = now_aware() + timedelta(hours=24 * 25)
        endDate = startDate + timedelta(hours=24)

        startDate = startDate.strftime("%Y-%m-%d")
        endDate = endDate.strftime("%Y-%m-%d")

        data = {
            "hotelId": 1,
            "startDate": startDate,
            "endDate": endDate,
            "email": "estate@email.com",
        }

        url = reverse("find_available_room")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), dict)

        for elem in response.data.values():
            self.assertEqual(type(elem), list)
            self.assertGreater(len(elem), 0)

    def test_date_order(self):
        for date in ["14", "15"]:
            data = {
                "hotelId": 1,
                "startDate": f"2023-09-{date}",
                "endDate": "2023-09-15",
                "email": "estate@email.com",
            }

            url = reverse("find_available_room")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 200 if date == "14" else 400)

    def test_is_overlapping(self):
        with transaction.atomic():
            room = Room.objects.get(pk=1)
            guest = Guest.objects.get(email="estate@email.com")
            start_date = now_aware() + timedelta(hours=4)
            end_date = start_date + timedelta(hours=50)

            reservation = define_new_reservation(
                guest=guest, room=room, check_in=start_date, check_out=end_date
            )
            reservation.save()

            # Test the case where the room is not overlapping
            overlapping = isOverlapping(
                room=room,
                start_date=end_date + timedelta(hours=150),
                end_date=end_date + timedelta(hours=200),
            )
            self.assertFalse(overlapping)

            # Test the cases where the room is overlapping
            overlapping = isOverlapping(
                room=room, start_date=start_date, end_date=end_date
            )
            self.assertTrue(overlapping)

            overlapping = isOverlapping(
                room=room, start_date=start_date - timedelta(hours=2), end_date=end_date
            )
            self.assertTrue(overlapping)

            overlapping = isOverlapping(
                room=room, start_date=start_date, end_date=end_date + timedelta(hours=2)
            )
            self.assertTrue(overlapping)

            overlapping = isOverlapping(
                room=room,
                start_date=start_date - timedelta(hours=2),
                end_date=end_date + timedelta(hours=2),
            )
            self.assertTrue(overlapping)

            reservation.delete()


class EnsureOneReservationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("ensure_one_reservation_per_guest")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_hotel_id_404(self):
        data = {"email": 1}
        url = reverse("ensure_one_reservation_per_guest")
        with self.assertRaises(KeyError):
            self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )

    def test_room_404(self):
        data = {"email": "estate@email.com", "hotelId": 1}
        url = reverse("ensure_one_reservation_per_guest")
        with self.assertRaises(KeyError):
            self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )

    def test_room_type_404(self):
        data = {"email": "estate@email.com", "hotelID": 1, "roomType": "Standard Room"}
        url = reverse("ensure_one_reservation_per_guest")
        with self.assertRaises(KeyError):
            self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )

    def test_email_404(self):
        data = {}
        url = reverse("ensure_one_reservation_per_guest")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_start_before_end(self):
        data = {
            "hotelId": 1,
            "roomType": "Standard Room",
            "roomId": 1,
            "email": "estate@email.com",
        }
        url = reverse("ensure_one_reservation_per_guest")

        ok_times = [
            (now_aware(), now_aware() + timedelta(days=4)),
            (now_aware() + timedelta(hours=3), now_aware() + timedelta(hours=30)),
        ]  # [(start , end)]

        incorrect_times = [
            (now_aware() - timedelta(days=4), now_aware()),
            (now_aware() - timedelta(days=4), now_aware() - timedelta(hours=5)),
            (now_aware(), now_aware() - timedelta(hours=5)),
            (now_aware() - timedelta(days=4), now_aware() - timedelta(hours=36)),
            (now_aware() - timedelta(days=4), now_aware() - timedelta(hours=5)),
            (now_aware() + timedelta(days=4), now_aware() + timedelta(hours=5)),
            (now_aware() + timedelta(days=4), now_aware()),
            (now_aware(), now_aware()),
        ]

        for time in ok_times:
            send = data
            s_t, e_t = time
            send["startDate"] = s_t.strftime("%Y-%m-%d")
            send["endDate"] = e_t.strftime("%Y-%m-%d")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            reservation = Reservation.objects.get(id=response.data)
            reservation.delete()

        for time in incorrect_times:
            send = data
            s_t, e_t = time
            send["startDate"] = s_t.strftime("%Y-%m-%d")
            send["endDate"] = e_t.strftime("%Y-%m-%d")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)

    def test_request_late(self):
        with transaction.atomic():
            room, _, _, end_datetime, reservation = define_reservation_comps()

            # Test the case where the room is not overlapping
            overlapping = isOverlapping(
                room=room,
                start_date=end_datetime + timedelta(hours=150),
                end_date=end_datetime + timedelta(hours=200),
            )
            self.assertFalse(overlapping)

            _, _, start_date, end_datetime, reservation1 = define_reservation_comps()

            # Test the case where the room is overlapping
            overlapping = isOverlapping(
                room=room,
                start_date=start_date,
                end_date=end_datetime,
            )
            self.assertTrue(overlapping)

            reservation.delete()
            reservation1.delete()

    def test_max_one_reservation(self):
        with transaction.atomic():
            # Guest has one PEND reservation already
            # and is creating another on the same room type
            # Note, that each hotel has its own room types
            (
                room1,
                guest,
                start_datetime,
                end_datetime,
                reservation1,
            ) = define_reservation_comps()

            startDate = start_datetime.strftime("%Y-%m-%d")
            endDate = end_datetime.strftime("%Y-%m-%d")

            data = {
                "hotelId": 1,
                "roomType": "Standard Room",
                "roomId": room1.id,
                "email": guest.email,
                "startDate": startDate,
                "endDate": endDate,
            }
            url = reverse("ensure_one_reservation_per_guest")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, reservation1.id)

            (
                room2,
                guest,
                start_datetime,
                end_datetime,
                reservation2,
            ) = define_reservation_comps()

            startDate = start_datetime.strftime("%Y-%m-%d")
            endDate = end_datetime.strftime("%Y-%m-%d")

            data = {
                "hotelId": 1,
                "roomType": "Standard Room",
                "roomId": room2.id,
                "email": guest.email,
                "startDate": startDate,
                "endDate": endDate,
            }
            url = reverse("ensure_one_reservation_per_guest")
            with self.assertRaises(ValueError):
                response = self.client.post(
                    url, data=json.dumps(data), content_type="application/json"
                )

            reservation1.delete()
            reservation2.delete()

    def test_guest_no_reservations(self):
        with transaction.atomic():
            (
                room,
                guest,
                start_datetime,
                end_datetime,
                reservation,
            ) = define_reservation_comps()
            reservation.delete()

            startDate = start_datetime.strftime("%Y-%m-%d")
            endDate = end_datetime.strftime("%Y-%m-%d")

            data = {
                "hotelId": 1,
                "roomType": "Standard Room",
                "roomId": room.id,
                "email": guest.email,
                "startDate": startDate,
                "endDate": endDate,
            }
            prev_res_count = Reservation.objects.count()

            url = reverse("ensure_one_reservation_per_guest")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(type(response.data), int)
            self.assertEqual(Reservation.objects.count(), prev_res_count + 1)

            reservation = Reservation.objects.get(pk=response.data)
            self.assertEqual(reservation.status, "PEND")

            reservation.delete()

    def test_guest_not_found(self):
        (
            room,
            guest,
            start_datetime,
            end_datetime,
            reservation,
        ) = define_reservation_comps()
        reservation.delete()

        startDate = start_datetime.strftime("%Y-%m-%d")
        endDate = end_datetime.strftime("%Y-%m-%d")

        data = {
            "hotelId": 1,
            "roomType": "Standard Room",
            "roomId": room.id,
            "email": "a@a.a",
            "startDate": startDate,
            "endDate": endDate,
        }

        url = reverse("ensure_one_reservation_per_guest")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)


class GetReservationInfoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("get_reservation_info")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_reservation_not_found(self):
        data = {"reservationID": -1}

        url = reverse("get_reservation_info")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_reservation_status_pend(self):
        with transaction.atomic():
            (
                _,
                _,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            reservation.status = "CNFR"
            reservation.save()

            data = {"reservationID": reservation.id}

            url = reverse("get_reservation_info")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, {"error": "Reservation not pending"})

            reservation.delete()

    def test_reservation_too_old(self):
        with transaction.atomic():
            (
                _,
                _,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            reservation.time_created = timezone.now() - timedelta(minutes=19)
            reservation.save()

            data = {"reservationID": reservation.id}

            url = reverse("get_reservation_info")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, {"error": "Reservation not found"})

            reservation.delete()

    def test_gets_info(self):
        with transaction.atomic():
            (
                _,
                _,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            data = {"reservationID": reservation.id}

            url = reverse("get_reservation_info")
            response = self.client.post(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            keys = [
                "id",
                "check_in_date_time",
                "check_out_date_time",
                "time_created",
                "time_modified",
                "total_price",
                "status",
                "guest",
                "room",
            ]
            for key in keys:
                self.assertIn(key, response.data)
            reservation.delete()


class IsUserAllowedTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("is_user_allowed")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_user_allowed(self):
        for i in range(2):
            with transaction.atomic():
                (
                    _,
                    guest,
                    _,
                    _,
                    reservation,
                ) = define_reservation_comps()

                if not i:
                    reservation.status = "CONF"
                    reservation.save()

                data = {"reservationID": reservation.id, "email": guest.email}

                url = reverse("is_user_allowed")
                response = self.client.post(
                    url, data=json.dumps(data), content_type="application/json"
                )
                self.assertEqual(response.status_code, 403 if not i else 200)
                reservation.delete()


class CancelReservationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_method(self):
        data = "{'email': 1,"
        url = reverse("cancel_reservation")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 405)

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("cancel_reservation")
        response = self.client.generic("DELETE", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_reservationID(self):
        data = {"reservationID": -1}
        url = reverse("cancel_reservation")
        response = self.client.delete(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_email(self):
        with transaction.atomic():
            (
                _,
                _,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            data = {"reservationID": reservation.id, "email": "guest.email"}

            url = reverse("cancel_reservation")
            response = self.client.delete(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 409)
            reservation.delete()

    def test_invalid_email(self):
        with transaction.atomic():
            (
                _,
                guest,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            data = {"reservationID": reservation.id, "email": guest.email}

            url = reverse("cancel_reservation")
            response = self.client.delete(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            reservation.delete()


class ReserveTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_invalid_method(self):
        data = "{'email': 1,"
        url = reverse("reserve")
        response = self.client.generic("POST", url, data=data)
        self.assertEqual(response.status_code, 405)

    def test_invalid_json(self):
        data = "{'email': 1,"
        url = reverse("reserve")
        response = self.client.generic("PATCH", url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invoice_already_made(self):
        with transaction.atomic():
            (
                _,
                guest,
                _,
                _,
                reservation,
            ) = define_reservation_comps()

            data = {"reservationID": reservation.id}
            invoice = InvoiceGuest.objects.create(
                guest=guest, reservation=reservation, invoice_amount=Decimal(10.99)
            )

            url = reverse("reserve")
            response = self.client.patch(
                url, data=json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)

            reservation.delete()
            invoice.delete()

    def test_reserves(self):
        with transaction.atomic():
            guest = Guest.objects.create(email="a@b.c")
            (
                _,
                g,
                _,
                _,
                reservation,
            ) = define_reservation_comps(email="a@b.c")

            invoice_count = InvoiceGuest.objects.count()
            
            data = {
                "success": "true",
                "reservationID": reservation.id,
                "firstName": "a",
                "lastName": "Jezty",
                "phoneNumber": "949133955",
                "country": "United Arab Emirates",
            }

            url = reverse("reserve")
            response = self.client.patch(
                url, data=json.dumps(data), content_type="application/json"
            )
            

            self.assertEqual(response.status_code, 200)
            self.assertEqual(guest.first_name , data["firstName"])
            self.assertEqual(guest.last_name , data["lastName"])
            self.assertEqual(guest.phone , data["phoneNumber"])
            self.assertEqual(guest.country.name , data["country"])
            self.assertEqual(InvoiceGuest.objects.count() , invoice_count + 1)


            reservation.delete()
            guest.delete()
            
