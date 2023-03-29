from django.urls import path
from .views import index, DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView, \
    DishTypeListView, DishTypeDetailView, DishTypeCreateView, DishTypeUpdateView, DishTypeDeleteView, CookListView, \
    CookDetailView, CookCreateView, CookUpdateView, CookDeleteView, toggle_assign_to_dish

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
    path("menu/types/delete/<int:pk>/", DishTypeDeleteView.as_view(), name="dish-type-delete"),

    path("menu/cooks/", CookListView.as_view(), name="cook-list"),
    path("menu/cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("menu/cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("menu/cooks/update/<int:pk>/", CookUpdateView.as_view(), name="cook-update"),
    path("menu/cooks/delete/<int:pk>/", CookDeleteView.as_view(), name="cook-delete"),
    path("menu/cooks/assign_to_dish/<int:pk>/", toggle_assign_to_dish, name="assign-to-dish"),

]


app_name = "menu"
