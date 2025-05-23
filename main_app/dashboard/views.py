from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from accounts.models import CustomUser
from content.models import ContentUserProfile, Post
from quiz.models import QuizAnswer
# Create your views here.

@login_required
def dashboard(request):
    posts = Post.objects.filter(post_user=request.user).order_by('-created_at')
    posts_count = posts.count()
    posts = posts[:3]
    user_profile = ContentUserProfile.objects.get(user=request.user)
    # Calculate total score in a single query
    top_three_users = CustomUser.objects.annotate(
        total_points=Count("quizanswer", filter=Q(quizanswer__is_correct=True)) * 10
    ).order_by("-total_points")[:3]

    user_total_points = QuizAnswer.objects.filter(user=request.user, is_correct=True).count() * 10
    context = {
        'posts': posts,
        'posts_count': posts_count,
        'user_profile': user_profile,
        'streak_target_percentage': (user_profile.current_streak / (user_profile.max_streak+10)) * 100 if user_profile.max_streak > 0 else 0,
        'leaderboard_users': top_three_users,
        'user_total_points': user_total_points,
    }
    return render(request, 'dashboard/dashboard.html', context)