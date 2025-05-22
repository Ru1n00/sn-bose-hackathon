from django.urls import path

from .views import (
    sign_in,
    sign_up,
    sign_out,
)

app_name = 'accounts'

urlpatterns = [
    path('sign-in/', sign_in, name='sign_in'),
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-out/', sign_out, name='sign_out'),
]