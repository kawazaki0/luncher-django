from django.urls import path

from luncher.meals.views import (
    meal_list_view,
)

app_name = "meals"
urlpatterns = [
    path("menu/", view=meal_list_view, name="list"),
]