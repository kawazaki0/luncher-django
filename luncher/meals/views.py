import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, FormView
from django.views.generic import TemplateView

from luncher.meals import usecase
from .forms import OrderMealForm
from .models import Meal

User = get_user_model()


class MealListView(ListView):
    model = Meal
    slug_field = "name"
    slug_url_kwarg = "name"
    templates_name = "meals/meal_list.html"
    queryset = Meal.objects.filter(date=datetime.date.today())


class OrderMealView(LoginRequiredMixin, FormView):
    form_class = OrderMealForm
    template_name = 'meals/meal_order_form.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Successful ordered")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('meals:list')


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class OrderHistoryView(LoginRequiredMixin, UserIsAdminMixin, TemplateView):
    template_name = 'meals/order_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from'] = self.request.GET.get('from')
        context['to'] = self.request.GET.get('to')

        if context['from'] and context['to']:
            history, total = usecase.get_order_history(context['from'],
                                                       context['to'],
                                                       restaurants=None)
            context['orders_history'] = history
            context['orders_total'] = total
        return context
