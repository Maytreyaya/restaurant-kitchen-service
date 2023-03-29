from django.urls import path
from .views import index, DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView, \
    DishTypeListView, DishTypeDetailView, DishTypeCreateView, DishTypeUpdateView, DishTypeDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("menu/", DishListView.as_view(), name="dish-list"),
    path("menu/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("menu/create/", DishCreateView.as_view(), name="dish-create"),
    path("menu/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("menu/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),

    path("menu/types/", DishTypeListView.as_view(), name="dish_type_list"),
    path("menu/types/<int:pk>/", DishTypeDetailView.as_view(), name="dish_type_detail"),
    path("menu/types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("menu/types/update/<int:pk>/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("menu/types/delete/<int:pk>/", DishTypeDeleteView.as_view(), name="dish-type-delete")

]


app_name = "menu"
