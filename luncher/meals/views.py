from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView

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
            raise ValidationError(
                "You don't have permissions to order meal.")  # TODO: return error in proper way.

        # inject authorized user into model
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('meals:list', kwargs={})


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
