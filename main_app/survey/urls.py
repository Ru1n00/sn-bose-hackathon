from django.urls import path

from .views import (
    survey_list,
)

app_name = 'survey'



urlpatterns = [
    path('survey/', survey_list, name='survey_list'),
]