import pendulum
from pendulum.exceptions import ParserError
from django.db import models

from luncher.users.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField()
    tel_number = models.CharField(max_length=20, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'restaurant'


class MealCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'meal_category'


class Meal(models.Model):
    name = models.CharField(max_length=1000)  # string
    category = models.ForeignKey(
        MealCategory, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(default=pendulum.today)

    def __str__(self):
        return '{} ({})'.format(self.name, self.category)

    class Meta:
        db_table = 'meal'


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {} ({})'.format(self.user, self.meal, self.timestamp)

    class Meta:
        db_table = 'user_order'


class MealImporter:
    SOUP = "Z"  # Zupa
    MEAL = "P"  # Posiłek
    EXTRA = "E"

    MEAL_MARKS = [SOUP, MEAL, EXTRA]

    PRICES = {
        SOUP: 4.00,
        MEAL: 12.00,
        EXTRA: 16.00,
    }

    def __init__(self, input_file):
        if isinstance(input_file, str):
            self.input_file = open(input_file, encoding='UTF-8', mode='r')
        else:
            self.input_file = input_file
        self.meals = []

    def parse(self):
        restaurant = None
        date = None
        counter = 1
        for line in self.input_file:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            if not line.strip():
                # skip empty lines
                continue
            if self.is_restaurant(line):
                restaurant = line.strip().lstrip('#').strip()
            if self.is_date(line):
                date = pendulum.from_format(line, "DD.MM.YYYY")
                counter = 1
            if self.is_meal(line):
                price = self.PRICES[line[0]]
                if line[0] == self.SOUP:
                    line = "ZUPA: {}".format(line[3:])
                if line[0] == self.EXTRA:
                    line = "EXTRA: {}".format(line[3:])
                if line[0] == self.MEAL:
                    line = "{}. {}".format(counter, line[3:])
                    counter += 1

                self.meals.append(Meal(
                    name=line, category=None,
                    restaurant=Restaurant.objects.filter(name=restaurant).get(),
                    price=price, date=date.format("YYYY-MM-DD"),
                ))

    def bulk_create(self):
        Meal.objects.bulk_create(self.meals)

    def is_restaurant(self, l):
        return l.strip().startswith('#')

    def is_meal(self, l):
        return len(l) > 0 and l[0] in self.MEAL_MARKS

    def is_date(self, l):
        try:
            pendulum.from_format(l, 'DD.MM.YYYY')
            return True
        except (ValueError, ParserError):
            return False
