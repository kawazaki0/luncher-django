from django.urls import path

from .views import UserDetailView, UserRedirectView, UserUpdateView, UserListView

app_name = "users"
urlpatterns = [
    path("", view=UserListView.as_view(), name="list"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("~update/", view=UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
]
