from django.test import TestCase

from menu.forms import CookCreationForm


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
