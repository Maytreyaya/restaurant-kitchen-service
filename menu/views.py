from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import DishForm, CookSearchForm, DishSearchForm, CookCreationForm, CookUpdateYearsForm, DishTypeSearchForm
from .models import Dish, DishType, Cook


# @login_required
def index(request):
    """View function for the home page of the site."""

    num_cookers = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cookers": num_cookers,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "menu/index.html", context=context)


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return Dish.objects.select_related("dish_type").filter(
                name__icontains=form.cleaned_data["name"]
            )


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("menu:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("menu:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("menu:dish-list")


class DishTypeListView(generic.ListView):
    model = DishType
    paginate_by = 5
    context_object_name = "dish_type_list"
    template_name = "menu/dish_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return DishType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "menu/dish_type_detail.html"
    queryset = DishType.objects.all().prefetch_related("dish_set__cookers")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("menu:dish_type_list")
    template_name = "menu/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "menu/dish_type_form.html"
    success_url = reverse_lazy("menu:dish_type_list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("menu:dish_type_list")
    template_name = "menu/dish_type_confirm_delete.html"


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = CookSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return Cook.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("menu:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateYearsForm
    success_url = reverse_lazy("menu:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("menu:cook-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cook.dishes.all()
    ):
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("menu:dish-detail", args=[pk]))






