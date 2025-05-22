from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Quiz, QuizAnswer

# Create your views here.
def submit_quiz_answer(request, post_slug):
    if request.method == "POST":
        post_quizes = Quiz.objects.filter(post__slug=post_slug)

        if not post_quizes.exists():
            messages.error(request, "No quiz available for this post.")
            return redirect("content:post_detail", slug=post_slug)

        for quiz in post_quizes:
            selected_option = request.POST.get(f"quiz_{quiz.id}")
            if selected_option:
                QuizAnswer.objects.create(user=request.user, quiz=quiz, selected_option=selected_option, is_correct=(selected_option == quiz.quizoption_set.first().answer))
        
        # Update user's streak
        user_profile = request.user.contentuserprofile
        user_profile.update_streak()
        
        messages.success(request, "Your answers have been submitted successfully.")
    return redirect("content:post_detail", slug=post_slug)

