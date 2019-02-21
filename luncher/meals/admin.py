from django.contrib import admin
from .models import Restaurant, MealCategory, Meal


admin.site.register(Restaurant)
admin.site.register(MealCategory)
admin.site.register(Meal)