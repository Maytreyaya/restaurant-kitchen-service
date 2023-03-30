from django.contrib.auth import get_user_model
from django.test import TestCase

from menu.models import DishType, Dish


class TestModels(TestCase):
    def test_dish_str(self) -> None:
        typeof = DishType.objects.create(name="Japan")

        dish = Dish.objects.create(name="Sushi", dish_type=typeof, price=67)

        self.assertEqual(str(dish), f"{dish.name} | {dish.price}")

    def test_create_cook_with(self) -> None:
        username = "Testill"
        password = "pastest"
        years = "5"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.years_of_experience, years)
