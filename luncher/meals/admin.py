from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from luncher.meals import models, usecase


class ActionMixin:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


class MealAdminInline(admin.TabularInline):
    model = models.Meal

    extra = 0
    readonly_fields = ('id_url', 'date')
    fields = ('id_url', 'name', 'category', 'price', 'date')
    show_full_result_count = False

    @mark_safe
    def id_url(self, obj):
        if not obj.id:
            return ''
        return '<a href="/admin/meals/meal/{}/change/">{}</a>'.format(obj.id, obj.id)

    id_url.allow_tags = True
    id_url.short_description = 'ID'


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].label = 'full address'
        self.fields['address'].widget = forms.Textarea(attrs={
            "rows": "0", "cols": "0", "style": "width: 99%; height: 90px;",
        })
        self.fields['name'].widget = forms.TextInput(attrs={"style": "width: 99%;"})

    def clean(self):
        # TODO(pawelzny): Validate form here
        return self.cleaned_data


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin, ActionMixin):
    form = RestaurantForm
    list_display = ('name', 'email', 'tel_number', 'min_purchase')
    list_filter = ('min_purchase',)
    search_fields = ('name', 'email', 'address')
    inlines = (MealAdminInline,)
    fieldsets = (
        (None, {
            'fields': [
                'name',
                ('min_purchase', 'email', 'tel_number'),
                'address',
            ],
            'classes': ['monospace'],
        }),
    )


@admin.register(models.MealCategory)
class MealCategoryAdmin(admin.ModelAdmin, ActionMixin):
    search_fields = ('name',)


# noinspection PyUnusedLocal
def order_meal(modeladmin, request, queryset):
    meals = list(queryset)
    price_total = sum([m.price for m in meals])

    if price_total > 16:
        raise ValidationError('price total must be lower or equal 16PLN but is {}'.format(price_total))

    orders = [models.UserOrder(user=request.user, meal=m) for m in meals]
    models.UserOrder.objects.bulk_create(orders)


order_meal.short_description = 'Order selected meals'


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin, ActionMixin):
    list_display = ('name', 'category', 'price', 'restaurant', 'date')
    list_filter = ('category', 'price', 'restaurant')
    search_fields = ('name', 'category', 'price', 'restaurant')
    readonly_fields = ('date',)
    fieldsets = (
        (None, {
            'fields': [
                ('name', 'category', 'price', 'restaurant', 'date'),
            ],
            'classes': ['monospace'],
        }),
    )
    actions = (order_meal,)
    actions_on_top = True
    actions_on_bottom = True


@admin.register(models.UserOrder)
class UserOrderAdmin(admin.ModelAdmin, ActionMixin):
    list_display = ('user', 'meal', 'meal_price', 'meal_restaurant', 'timestamp')
    search_fields = ('user', 'meal')
    fieldsets = (
        (None, {
            'fields': [
                ('user', 'timestamp'),
                ('meal', 'meal_price', 'meal_restaurant'),
            ],
            'classes': ['monospace'],
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ('meal_price', 'meal_restaurant', 'timestamp')
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ('user', 'meal_price', 'meal_restaurant', 'timestamp')
        return super().change_view(request, object_id, form_url, extra_context)

    def meal_price(self, obj):
        return '{} PLN'.format(obj.meal.price)

    meal_price.short_description = 'meal price'

    def meal_restaurant(self, obj):
        return obj.meal.restaurant

    meal_restaurant.short_description = 'restaurant'

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # superuser can do everything
            return obj.save()

        if not request.user.can_order_meal:
            raise ValidationError("you can't order meal, get in touch with your supervisor")

        if change is False and not usecase.is_user_able_to_order_meal():
            # if this is create request and user can't order meal
            raise ValidationError("can't order meal past 11")

        obj.save()
