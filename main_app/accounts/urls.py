from django.urls import path

from .views import (
    sign_in,
)

app_name = 'accounts'

urlpatterns = [
    path('sign-in/', sign_in, name='sign_in')
]