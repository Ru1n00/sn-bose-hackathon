from django.urls import path

from .views import (
    survey_list,
    survey_detail,
)

app_name = 'survey'



urlpatterns = [
    path('survey/', survey_list, name='survey_list'),
    path('survey-detail/', survey_detail, name='survey_detail'),
]