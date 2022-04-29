from django.conf import settings
from django.db import models


ORDER_BY_CHOICES = (
    ("price_asc", "Price Asc"),
    ("price_desc", "Price Desc"),
)

CAR_MARK = (
    ("bmw", "BMW"),
    ("merc", "MERCEDES"),
    ("toyo", "TOYOTA"),
)


ENGINE_TYPE = (
    ("petr", "Petrol"),
    ("dies", "Diesel"),
    ("hyb", "Hybrid"),
    ("elec", "Electro"),
)


DRIVE = (
    ("fwd", "Front-wheel drive"),
    ("rwd", "Rear-wheel drive"),
    ("awd", "Automatic 4WD"),
    ("4wd", "Full-time 4WD"),
)


GEAR_BOX = (
    ("auto", "Automatic"),
    ("man", "Manual"),
)


class Advert(models.Model):
    engine_type = models.CharField(max_length=100, choices=ENGINE_TYPE, default="No type")
    engine_capacity = models.IntegerField(default="No capacity")
    drive = models.CharField(max_length=100, choices=DRIVE, default="No type")
    gear_box = models.CharField(max_length=100, choices=GEAR_BOX, default="No type")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    win = models.CharField(max_length=17, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    price_usd = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adverts"
    )
    phone_number = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_adverts"
    )
    honey = models.CharField(max_length=200, default=None)


class Canary(models.Model):
    table = models.TextField(max_length=300)
    canary = models.CharField(max_length=500)
