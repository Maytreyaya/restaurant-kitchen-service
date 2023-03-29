from django.db import models
from django.contrib.auth.models import AbstractUser


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:

        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "cookers"

    def __str__(self) -> str:
        return (f"{self.username}"
                f" | {self.first_name} {self.last_name}"
                f" | {self.years_of_experience}")


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cookers = models.ManyToManyField(Cook, related_name="dishes")

    class Meta:
        verbose_name_plural = "dishes"

    def __str__(self) -> str:
        return f"{self.name} | {self.price}"
