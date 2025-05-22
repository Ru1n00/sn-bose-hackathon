from django.contrib import admin
from .models import Quiz, QuizOption, QuizAnswer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("question", "post", "created_at")
    search_fields = ("question", "post__title")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"

@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "option_a", "option_b", "option_c", "option_d", "answer")
    search_fields = ("quiz__question", "option_a", "option_b", "option_c", "option_d")
    list_filter = ("quiz",)

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "selected_option", "is_correct", "created_at")
    search_fields = ("quiz__question", "user__email", "selected_option")
    list_filter = ("is_correct", "created_at")
    date_hierarchy = "created_at"
