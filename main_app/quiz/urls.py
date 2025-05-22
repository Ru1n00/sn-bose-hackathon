from django.urls import path

from .views import submit_quiz_answer


app_name = 'quiz'

urlpatterns = [
    path('submit_quiz_answer/<str:post_slug>/', submit_quiz_answer, name='submit_quiz_answer'),
]
