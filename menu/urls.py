from django.urls import path
from .views import index, DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("menu/", DishListView.as_view(), name="dish-list"),
    path("menu/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("menu/create/", DishCreateView.as_view(), name="dish-create"),
    path("menu/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("menu/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),

]


app_name = "menu"
