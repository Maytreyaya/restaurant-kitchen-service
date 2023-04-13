from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from menu.forms import CookCreationForm, DishTypeSearchForm, DishSearchForm, DishForm
from menu.models import DishType


class TestForms(TestCase):
    def test_cook_years_valid_input(self) -> None:
        form_data = {
            "username": "Testill",
            "first_name": "Test",
            "last_name": "Testovich",
            "password1": "pastest456",
            "password2": "pastest456",
            "years_of_experience": 10,
        }
        form = CookCreationForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_years_invalid_input(self) -> None:
        form_data = {
            "username": "Testill",
            "first_name": "Test",
            "last_name": "Testovich",
            "password1": "pastest456",
            "password2": "pastest456",
            "years_of_experience": 687,
        }
        form = CookCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_valid_form_data(self):

        form_data = {
            "name": "Italian",
        }

        form = DishTypeSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["name"], "Italian")

    def test_empty_form_data(self):
        form_data = {}

        form = DishSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["name"], "")

class DishFormTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="password"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="password"
        )

    def test_cookers_field_widget(self):
        form = DishForm()

        self.assertIsInstance(form.fields["cookers"].widget, forms.CheckboxSelectMultiple)

    def test_valid_form_data(self):
        dish_type = DishType.objects.create(name="Italian")
        form_data = {
            "name": "Spaghetti Carbonara",
            "dish_type": dish_type,
            "description": "A classic pasta dish from Italy",
            "cookers": [self.user1.id, self.user2.id],
            "price": "98",
        }

        form = DishForm(data=form_data)

        self.assertTrue(form.is_valid())

        dish = form.save()
        self.assertEqual(dish.name, "Spaghetti Carbonara")
        self.assertEqual(dish.price, 98)
        self.assertEqual(dish.description, "A classic pasta dish from Italy")
        self.assertEqual(set(dish.cookers.all()), {self.user1, self.user2})

    def test_empty_form_data(self):
        form_data = {}

        form = DishForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn("name", form.errors)
        self.assertEqual(len(form.errors["name"]), 1)
        self.assertEqual(form.errors["name"][0], "This field is required.")
