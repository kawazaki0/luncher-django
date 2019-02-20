from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from luncher.users.forms import UserChangeForm, UserCreationForm
from luncher.users.models import Location

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'alias', 'first_name', 'last_name', 'email', 'is_superuser', 'is_active')
    search_fields = ('username', 'alias', 'first_name', 'last_name')
    fieldsets = (
        ('User', {
            'fields': [
                'alias',
                'location'
            ],
        }),
    ) + auth_admin.UserAdmin.fieldsets


# TODO(pawelzny): import locations from file

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': [
                ('name', 'is_active'),
            ],
        }),
    )
