from base.models import *
from .helpful_test_functions import *

from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
import io

from datetime import datetime
from decimal import Decimal


class CountryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="United States")

    def test_country_creation(self):
        """Test if the country is created correctly"""
        self.assertEqual(self.country.name, "United States")

    def test_country_str_representation(self):
        """Test the string representation of the country"""
        self.assertEqual(str(self.country), "United States")

    def test_country_verbose_name_plural(self):
        """Test the verbose name plural of the country model"""
        self.assertEqual(Country._meta.verbose_name_plural, "Countries")


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="Test Country")
        cls.city = City.objects.create(name="Test City", country=cls.country)

    def test_city_name(self):
        city_name = self.city.name
        self.assertEqual(city_name, "Test City")

    def test_city_country(self):
        city_country = self.city.country
        self.assertEqual(city_country, self.country)

    def test_city_str_representation(self):
        city_str = str(self.city)
        self.assertEqual(city_str, "Test City")

    def test_city_verbose_name_plural(self):
        verbose_name_plural = City._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "Cities")


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Test Category")

    def test_category_name(self):
        category_name = self.category.name
        self.assertEqual(category_name, "Test Category")

    def test_category_str_representation(self):
        category_str = str(self.category)
        self.assertEqual(category_str, "Test Category")

    def test_category_verbose_name_plural(self):
        verbose_name_plural = Category._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "Categories")


class HotelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Test Category")
        cls.city = City.objects.create(name="Test City")

    def setUp(self):
        self.hotel = define_new_hotel(self=self)
        self.hotel.save()

    def test_hotel_name(self):
        hotel_name = self.hotel.name
        self.assertEqual(hotel_name, "Test Hotel")

    def test_hotel_city(self):
        hotel_city = self.hotel.city
        self.assertEqual(hotel_city, self.city)

    def test_hotel_category(self):
        hotel_category = self.hotel.category
        self.assertEqual(hotel_category, self.category)

    def test_invalid_star_rating(self):
        validators = [
            v.__class__.__name__
            for v in self.hotel._meta.get_field("star_rating").validators
        ]
        self.assertIn("MinValueValidator", validators)
        self.assertIn("MaxValueValidator", validators)

        invalid_star_ratings = [-1, 6, -10, 100]
        create_model_testcase(
            self=self,
            test_case_array=invalid_star_ratings,
            model_field="star_rating",
            curr_instance=self.hotel,
            new_instance_func=define_new_hotel,
        )

    def test_hotel_service(self):
        # The service field is a PositiveSmallIntegerField
        validators = [
            v.__class__.__name__
            for v in self.hotel._meta.get_field("service").validators
        ]
        self.assertIn("MinValueValidator", validators)
        self.assertIn("MaxValueValidator", validators)

        invalid_services = [-1, 5, 10 ** 5]
        create_model_testcase(
            self=self,
            test_case_array=invalid_services,
            model_field="service",
            curr_instance=self.hotel,
            new_instance_func=define_new_hotel,
        )

    def test_hotel_review_count(self):
        hotel_review_count = self.hotel.review_count
        self.assertEqual(hotel_review_count, 10)

        validators = [
            v.__class__.__name__
            for v in self.hotel._meta.get_field("review_count").validators
        ]
        self.assertIn("MinValueValidator", validators)

        # Using a negative integer only and not a float aswell
        # because the review_count field is defined as a PositiveIntegerField,
        # which only accepts non-negative integer values.
        # When passing a float value like 0.5 or -0.5 to the review_count field,
        # Django converts it to an integer by rounding towards zero.
        invalid_review_count = [-1]
        create_model_testcase(
            self=self,
            test_case_array=invalid_review_count,
            model_field="review_count",
            curr_instance=self.hotel,
            new_instance_func=define_new_hotel,
        )

    def test_hotel_review_rating_range(self):
        validators = [
            v.__class__.__name__
            for v in self.hotel._meta.get_field("review_rating").validators
        ]
        self.assertIn("MinValueValidator", validators)
        self.assertIn("MaxValueValidator", validators)

        invalid_review_ratings = [-1, 10 ** 5]
        create_model_testcase(
            self=self,
            test_case_array=invalid_review_ratings,
            model_field="review_rating",
            curr_instance=self.hotel,
            new_instance_func=define_new_hotel,
        )

    def test_hotel_str_representation(self):
        hotel_str = str(self.hotel)
        self.assertEqual(hotel_str, "Test Hotel")


class HotelDescriptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_test_data(cls)

        cls.description = "Sample hotel description"
        cls.hotel_description = HotelDescription.objects.create(
            hotel=cls.hotel, description=cls.description
        )

    def test_hotel_description_str(self):
        expected_str = self.hotel.name
        self.assertEqual(str(self.hotel_description), expected_str)

    def test_hotel_description_relationship(self):
        self.assertEqual(self.hotel_description.hotel, self.hotel)
        self.assertEqual(self.hotel.hotel_description, self.hotel_description)

    def test_description_unique(self):
        with self.assertRaises(IntegrityError):
            HotelDescription.objects.create(
                hotel=self.hotel, description="Test description"
            )


class RoomTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_test_data(cls)

    def setUp(self):
        self.room_type = define_new_room_type(self=self)
        self.room_type.save()

    def test_room_type_str(self):
        expected_str = "Standard Room"
        self.assertEqual(str(self.room_type), expected_str)

        with self.assertRaises(ValidationError):
            string_longer_50 = "012345678901234567890123456789012345678901234567891"
            self.room_type.name = string_longer_50
            self.room_type.full_clean()

    def test_room_type_fields(self):
        self.assertEqual(self.room_type.hotel, self.hotel)
        self.assertEqual(self.room_type.name, "Standard Room")
        self.assertEqual(self.room_type.description, "A standard room description")
        self.assertEqual(self.room_type.current_price, Decimal("99.99"))
        self.assertEqual(self.room_type.stripe_price_id, "price_123")
        self.assertTrue(
            any(
                isinstance(validator, MinValueValidator)
                for validator in self.room_type._meta.get_field(
                    "current_price"
                ).validators
            )
        )
        self.assertEqual(
            self.room_type._meta.get_field("current_price").default,
            Decimal("999999.99"),
        )

    def test_current_price_range(self):
        invalids = {
            "invalid_digits": [123456789.00],
            "invalid_value": [-1, -1.2],
        }
        for key in invalids:
            create_model_testcase(
                self=self,
                test_case_array=invalids[key],
                model_field="current_price",
                curr_instance=self.room_type,
                new_instance_func=define_new_room_type,
            )


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_test_data(cls)

    def setUp(self):
        self.room_type = define_new_room_type(self=self)
        self.room_type.save()

    def test_room_creation(self):
        room = Room.objects.create(
            name="Room 101",
            room_type=self.room_type,
        )

        self.assertEqual(room.name, "Room 101")
        self.assertEqual(room.room_type, self.room_type)


class GuestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_test_data(cls)

    def setUp(self):
        self.guest = Guest(
            email="test@example.com",
            country=self.country,
            first_name="John",
            last_name="Doe",
            phone="1234567890",
        )

    def test_guest_creation(self):
        # Create a valid Guest object

        # Validate and save the Guest object
        self.guest.full_clean()
        self.guest.save()

        # Retrieve the saved Guest object from the database
        saved_guest = Guest.objects.get(email="test@example.com")

        # Perform assertions to verify the data
        self.assertEqual(saved_guest.email, "test@example.com")
        self.assertEqual(saved_guest.country, self.country)
        self.assertEqual(saved_guest.first_name, "John")
        self.assertEqual(saved_guest.last_name, "Doe")
        self.assertEqual(saved_guest.phone, "1234567890")

    def test_invalid_guest_creation(self):
        # Attempt to create a Guest object with missing required fields
        guest = Guest(
            email="test@example.com",
            country=None,  # Missing required field
            first_name="John",
            last_name="",  # Empty required field
            phone="",
        )

        # Validate and expect a ValidationError to be raised
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_guest_email(self):
        invalid_emails = ["a.c", "a@b", "a", "a@" ".", ".com", "@."]
        create_model_testcase(
            self=self,
            test_case_array=invalid_emails,
            model_field="email",
            curr_instance=self.guest,
            new_instance_func=define_new_guest,
        )

    def test_guest_values_length(self):
        first_name = "123456789012345678901234567890123456789012345678901"  # 51 chars
        last_name = "123456789012345678901234567890123456789012345678901"  # 51 chars
        phone = "1234567890123456789012345678901"  # 31 chars

        g = define_new_guest(
            self=self, first_name=first_name, last_name=last_name, phone=phone
        )
        with self.assertRaises(ValidationError):
            g.full_clean()


class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        reservation_invoice_setup(cls=cls)

    def setUp(self) -> None:
        self.reservation = define_new_reservation(self=self)

    def test_reservation_creation(self):
        check_in = datetime(2023, 1, 1, 14, 0)
        check_out = datetime(2023, 1, 3, 10, 0)

        check_in = timezone.make_aware(check_in, timezone.get_current_timezone())
        check_out = timezone.make_aware(check_out, timezone.get_current_timezone())

        total_price = Decimal("199.98")

        reservation = Reservation(
            guest=self.guest,
            room=self.room,
            check_in_date_time=check_in,
            check_out_date_time=check_out,
            total_price=total_price,
            status="CNFR",
        )

        # Validate and save the Reservation object
        reservation.full_clean()
        reservation.save()

        # Perform assertions to verify the created reservation
        self.assertEqual(reservation.guest, self.guest)
        self.assertEqual(reservation.room, self.room)
        self.assertEqual(reservation.check_in_date_time, check_in)
        self.assertEqual(reservation.check_out_date_time, check_out)
        self.assertEqual(reservation.total_price, total_price)
        self.assertEqual(reservation.status, "CNFR")

    def test_invalid_total_price(self):
        invalid_prices = [-1, -10, 123456789.00]

        create_model_testcase(
            self=self,
            test_case_array=invalid_prices,
            model_field="total_price",
            curr_instance=self.reservation,
            new_instance_func=define_new_reservation,
        )

    def test_invalid_status(self):
        invalid_statuses = ["PND", "can", "idk"]

        create_model_testcase(
            self=self,
            test_case_array=invalid_statuses,
            model_field="status",
            curr_instance=self.reservation,
            new_instance_func=define_new_reservation,
        )

    def test_default_status(self):
        self.assertEqual(self.reservation.status, "PEND")

    def test_str_representation(self):
        self.assertEqual(str(self.reservation), self.guest.email)



class InvoiceGuestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        reservation_invoice_setup(cls=cls)

        cls.reservation = define_new_reservation(guest=cls.guest, room=cls.room)
        cls.reservation.save()
    
    def setUp(self) -> None:
        self.invoice = InvoiceGuest(
            guest=self.guest,
            reservation=self.reservation,
            invoice_amount=Decimal("99.99"),
        )

    def test_invoice_creation(self):
        invoice_amount = Decimal("199.99")

        invoice = InvoiceGuest(
            guest=self.guest,
            reservation=self.reservation,
            invoice_amount=invoice_amount,
        )

        # Validate and save the InvoiceGuest object
        invoice.full_clean()
        invoice.save()

        # Perform assertions to verify the created invoice
        self.assertEqual(invoice.guest, self.guest)
        self.assertEqual(invoice.reservation, self.reservation)
        self.assertEqual(invoice.invoice_amount, invoice_amount)

    def test_invalid_invoice_amount(self):
        invalid_amounts = [-1, -10, 123456789]

        for amount in invalid_amounts:
            with self.assertRaises(ValidationError):
                self.invoice.invoice_amount = Decimal(amount)
                self.invoice.full_clean()

    def test_canceled_invoice(self):
        canceled_time = now_aware()

        invoice = InvoiceGuest(
            guest=self.guest,
            reservation=self.reservation,
            invoice_amount=Decimal("199.99"),
            time_canceled=canceled_time,
        )

        # Validate and save the InvoiceGuest object
        invoice.full_clean()
        invoice.save()

        # Perform assertion to verify the canceled time
        self.assertEqual(invoice.time_canceled, canceled_time)

    def test_str_representation(self):
        invoice = InvoiceGuest(
            guest=self.guest,
            reservation=self.reservation,
            invoice_amount=Decimal("199.99"),
        )

        # Perform assertion to verify the string representation
        self.assertEqual(str(invoice), self.guest.email)





class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hotel = Hotel.objects.create(name="Test Hotel")

    def test_image_creation(self):
        # Create a test image file
        image = PILImage.new("RGB", (100, 100))
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="WEBP")
        image_file = SimpleUploadedFile(
            name="test_image.webp", content=image_bytes.getvalue(), content_type="image/webp"
        )

        # Create an Image instance
        image_instance = Image(hotel=self.hotel, image=image_file)

        # Validate and save the Image object
        image_instance.full_clean()
        image_instance.save()

        # Perform assertions to verify the created image
        self.assertEqual(image_instance.hotel, self.hotel)

    def test_invalid_image_file(self):
        invalid_image_file = SimpleUploadedFile(
            name="test_image.png", content=b"Invalid image file", content_type="image/png"
        )

        with self.assertRaises(ValidationError):
            image_instance = Image(hotel=self.hotel, image=invalid_image_file)
            image_instance.full_clean()

    def test_str_representation(self):
        image_instance = Image(hotel=self.hotel)

        # Perform assertion to verify the string representation
        self.assertEqual(str(image_instance), self.hotel.name)
