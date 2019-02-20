from django.contrib.auth import get_user_model
from django.views.generic import ListView

from luncher.meals.models import Meal

User = get_user_model()


class MealListView(ListView):
    model = Meal
    slug_field = "name"
    slug_url_kwarg = "name"
    templates_path = "templates/meals/meal_list.html"


meal_list_view = MealListView.as_view()
