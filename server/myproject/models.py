from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Dealer(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True, db_index=True)
    address = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class DealerReview(models.Model):
    dealer_id = models.PositiveIntegerField(db_index=True)
    reviewer_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=1) & Q(rating__lte=5),
                name="dealer_review_rating_1_to_5",
            ),
        ]

    def __str__(self):
        return f"Review for dealer {self.dealer_id} by {self.reviewer_name}"


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models",
    )
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["make", "name"],
                name="unique_car_model_per_make",
            ),
        ]

    def __str__(self):
        return f"{self.make.name} {self.name}"
