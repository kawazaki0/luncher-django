from django.urls import path

from .views import MealListView, OrderHistoryView, OrderMealView

app_name = "meals"
urlpatterns = [
    path("", view=MealListView.as_view(), name="list"),
    path("order", view=OrderMealView.as_view(), name='order'),
    path("order/history", view=OrderHistoryView.as_view(), name='order_history'),
]
