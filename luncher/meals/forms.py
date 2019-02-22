from django.forms import ModelForm

from .models import UserOrder


class OrderMealForm(ModelForm):
    class Meta:
        model = UserOrder
        fields = ('meal', )
