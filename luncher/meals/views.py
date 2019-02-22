from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from luncher.meals import usecase
from .forms import OrderMealForm
from .models import Meal

User = get_user_model()


class MealListView(ListView):
    model = Meal
    slug_field = "name"
    slug_url_kwarg = "name"
    templates_name = "meals/meal_list.html"


class OrderMealView(LoginRequiredMixin, CreateView):
    form_class = OrderMealForm
    template_name = 'meals/meal_order_form.html'

    def form_valid(self, form):
        if not self.request.user.can_order_meal or not usecase.is_user_able_to_order_meal():
            raise ValidationError("You don't have permissions to order meal.")  # TODO: return error in proper way.

        # inject authorized user into model
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('meals:list', kwargs={})
