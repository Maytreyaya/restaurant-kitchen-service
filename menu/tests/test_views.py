from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from menu.models import Dish, DishType, Cook


COOK_URL = reverse("menu:cook-list")
DISH_URL = reverse("menu:dish-list")
DISH_TYPE_URL = reverse("menu:dish_type_list")


class PrivateDishTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="cooker",
            password="testcook"
        )
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(
            name="Brazil",
        )
        Dish.objects.create(name="Baklazhan", price="4", dish_type=dish_type)
        Dish.objects.create(name="Lemon", price="4", dish_type=dish_type)
        Dish.objects.create(name="Banana", price="4", dish_type=dish_type)

    def test_get_dish_list(self) -> None:
        res = self.client.get(DISH_URL)

        cars = Dish.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "menu/dish_list.html")

    def test_search_dish(self) -> None:
        key = "e"
        response = self.client.get(reverse("menu:dish-list") + f"?name={key}")

        dish_list = Dish.objects.filter(name__icontains=key)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dish_list)
        )


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="mrcooker",
            password="testcook"
        )
        self.client.force_login(self.user)
        Cook.objects.create(username="test1",
                            password="pastest1",
                            years_of_experience=5)
        Cook.objects.create(username="test2",
                            password="pastest2",
                            years_of_experience=3)

    def test_get_dish_list(self) -> None:
        res = self.client.get(COOK_URL)

        cookers = Cook.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["cook_list"]),
            list(cookers)
        )
        self.assertTemplateUsed(res, "menu/cook_list.html")

    def test_search_cook_with_username(self) -> None:
        key = "mr"
        response = self.client.get(reverse("menu:cook-list")
                                   + f"?username={key}")

        cookers = Cook.objects.filter(username__icontains=key)
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cookers)
        )


class PrivateDishTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test-driver",
            password="testdriver"
        )
        self.client.force_login(self.user)

        DishType.objects.create(name="Germany")
        DishType.objects.create(name="Italy")
        DishType.objects.create(name="Japan")

    def test_get_dish_type_list(self) -> None:
        res = self.client.get(DISH_TYPE_URL)

        dishes = DishType.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_type_list"]),
            list(dishes)
        )
        self.assertTemplateUsed(res, "menu/dish_type_list.html")

    def test_search_dish_type_with_name(self) -> None:
        key = "i"
        response = self.client.get(reverse("menu:dish_type_list")
                                   + f"?name={key}")

        dish_list = DishType.objects.filter(name__icontains=key)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_list)
        )


class DishCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.url = reverse("menu:dish-create")
        self.data = {
            "name": "Test Dish",
            "description": "This is a test dish.",
            "price": 9.99,
        }

    def test_logged_in_user_can_create_dish(self):
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_create_dish(self):
        self.client.logout()

        response = self.client.post(self.url, data=self.data)

        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_invalid_form_submission_returns_errors(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "name", "This field is required.")
        self.assertFormError(response, "form", "price", "This field is required.")

    def test_view_uses_correct_template(self):
        url = reverse("menu:dish-create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "menu/dish_form.html")

    def test_view_url_accessible_by_name(self):
        url = reverse("menu:dish-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CookCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("menu:cook-create")
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.data = {
            "username": "testcook",
            "password1": "testpass123",
            "password2": "testpass123",
            "years_of_experience": "8",
        }

    def test_logged_in_user_can_create_cook(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cook.objects.filter(username="testcook").exists())

    def test_unauthenticated_user_cannot_create_cook(self):
        response = self.client.post(self.url, data=self.data)

        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class CookDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.cook = Cook.objects.create(username="testcook", password="testpass123")
        self.url = reverse("menu:cook-delete", args=[self.cook.id])

    def test_logged_in_user_can_delete_cook(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cook.objects.filter(username="testcook").exists())

    def test_unauthenticated_user_cannot_delete_cook(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_cook_does_not_exist_after_deletion(self):
        self.client.login(username="testuser", password="testpass")

        self.client.post(self.url)

        self.assertFalse(Cook.objects.filter(username="testcook").exists())
