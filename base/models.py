from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from decimal import Decimal


@deconstructible
class WebpValidator:
    def __call__(self, value):
        if not value.name.endswith('.webp'):
            raise ValidationError('Only .webp images are allowed.')




# Geographical location section ↓
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="country_cities", null=True
    )

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


# Hotels and rooms section ↓
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="city_hotels", null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_hotels", null=True
    )
    star_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True
    )
    service = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], null=True
    )
    review_count = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)
    review_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0
    )

    def __str__(self):
        return self.name


class HotelDescription(models.Model):
    hotel = models.OneToOneField(
        Hotel, on_delete=models.CASCADE, related_name="hotel_description", null=True
    )
    description = models.TextField(null=True)

    def __str__(self):
        return self.hotel.name


class RoomType(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="hotel_room_types"
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    current_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal("999999.99"),
    )
    stripe_price_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room_type_rooms", null=True
    )

    def __str__(self):
        return self.name


# Guest and reservation section ↓
class Guest(models.Model):
    email = models.EmailField(primary_key=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="country_guests", null=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="guest_reservations"
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_reservations", null=True
    )
    check_in_date_time = models.DateTimeField()
    check_out_date_time = models.DateTimeField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    STATUS_CHOICES = [
        ("PEND", "Pending"),
        ("CNCL", "Cancelled"),
        ("CNFR", "Confirmed"),
    ]
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default="PEND")

    def __str__(self):
        return self.guest.email


class InvoiceGuest(models.Model):
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="guest_invoices"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="reservation_invoices"
    )
    time_paid = models.DateTimeField(auto_now_add=True)
    time_canceled = models.DateTimeField(blank=True, null=True)
    invoice_amount = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.guest.email


class Image(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, null=True, related_name="hotel_images"
    )
    image = models.ImageField(upload_to="images", validators=[WebpValidator()], null=True)

    def __str__(self):
        return self.hotel.name

