from decimal import Decimal

import pendulum
from django.db.models import Sum

from luncher.meals.models import Restaurant, UserOrder


def is_it_time_to_make_orders():
    threshold_time = pendulum.today('UTC').set(hour=11)
    now = pendulum.now('UTC')
    return now <= threshold_time


class OrderHistoryPayment:
    def __init__(self, restaurant, payments):
        self.restaurant = restaurant
        if payments is None:
            self.payments = Decimal(0)
        else:
            self.payments = payments

    def __str__(self):
        return '{}: {}'.format(self.restaurant, self.payments)


def get_order_history(from_date, to_date, restaurants):
    if restaurants is None:
        restaurants = list(Restaurant.objects.distinct().values_list('name', flat=True))

    order_history = []
    for restaurant in restaurants:
        money_spent = UserOrder.objects.filter(
            meal__date__gte=from_date,
            meal__date__lte=to_date,
            meal__restaurant__name=restaurant).aggregate(Sum('meal__price'))

        order_history.append(OrderHistoryPayment(restaurant, money_spent['meal__price__sum']))

    total_payments = sum([h.payments for h in order_history])
    return sorted(order_history, key=lambda x: x.restaurant), total_payments
