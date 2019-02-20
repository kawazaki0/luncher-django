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
    category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.category)

    class Meta:
        db_table = 'meal'


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {} ({})'.format(self.user, self.meal, self.timestamp)

    class Meta:
        db_table = 'user_order'
