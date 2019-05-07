import pendulum
from django.forms import Form, IntegerField, ValidationError

from luncher.meals import usecase
from .models import Meal, UserOrder


class OrderMealForm(Form):
    chosen_meals = None
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(OrderMealForm, self).__init__(*args, **kwargs)
        for i, q in enumerate(Meal.objects.filter(date=pendulum.today())):
            label = f"{q.name} ({q.price} PLN)"
            self.declared_fields[f'{q.pk}'] = IntegerField(
                initial=0, min_value=0, label=label, required=False)

    def clean(self):
        cleaned_data = super().clean()

        if not self.user.can_order_meal:
            raise ValidationError("You have inactive account. Permission denied.")

        if not usecase.is_it_time_to_make_orders():
            raise ValidationError("Sorry, you are too late. Time for order expired.")

        if self._calculate_summary_price() > 16:  # TODO: Move this number to django settings
            raise ValidationError('Summary price over limit')

        return cleaned_data

    def _calculate_summary_price(self):
        pks = [
            meal_id for meal_id, quantity in self.cleaned_data.items()
            if quantity not in (None, 0)
        ]
        summary_price = 0
        self.chosen_meals = Meal.objects.filter(pk__in=pks)
        for meal in self.chosen_meals:
            summary_price += meal.price * self.cleaned_data[str(meal.pk)]
        return summary_price

    def save(self):
        # delete old orders
        UserOrder.objects.filter(timestamp__date=pendulum.today(), user=self.user).delete()
        # create the current one
        UserOrder.objects.bulk_create([UserOrder(user=self.user, meal=m, quantity=self.cleaned_data[str(m.pk)])
                                       for m in self.chosen_meals])
