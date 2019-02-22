from django.urls import path

from .views import MealListView, OrderMealView

app_name = "meals"
urlpatterns = [
    path("", view=MealListView.as_view(), name="list"),
    path("order", view=OrderMealView.as_view(), name='order')
]
