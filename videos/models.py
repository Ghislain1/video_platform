
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Video(models.Model):
    class AccessType(models.TextChoices):
        FREE = "free", "Free"
        PAID = "paid", "Paid"

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="videos",
    )

    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
    )

    access_type = models.CharField(
        max_length=10,
        choices=AccessType.choices,
        default=AccessType.FREE,
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        super().clean()

        if self.price < Decimal("0.00"):
            raise ValidationError({
                "price": "The price cannot be negative."
            })

        if (
            self.access_type == self.AccessType.FREE
            and self.price != Decimal("0.00")
        ):
            raise ValidationError({
                "price": "Free videos must have a price of 0."
            })

        if (
            self.access_type == self.AccessType.PAID
            and self.price <= Decimal("0.00")
        ):
            raise ValidationError({
                "price": "Paid videos must have a price greater than 0."
            })

    def __str__(self):
        return self.title