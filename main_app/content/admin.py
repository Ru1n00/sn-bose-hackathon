from django.contrib import admin
from .models import (
    Category, 
    ContentUserProfile, 
    Post, 
    PostRating, 
    PostReport, 
    PostFile, 
    PostComment
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(ContentUserProfile)
class ContentUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "stage", "current_streak", "max_streak", "last_activity", "get_contributions")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("stage", "last_activity")

class PostFileInline(admin.StackedInline):
    model = PostFile
    extra = 1  # Number of empty file upload fields to show
    readonly_fields = ("file_type",)  # Make file type non-editable


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_user", "category", "upvotes", "downvotes", "report_count", "created_at", "is_active")
    search_fields = ("title", "post_user__email")
    list_filter = ("category", "stage", "is_active", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"

    inlines = [PostFileInline]

@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "rating", "created_at")
    search_fields = ("post__title", "user__email")
    list_filter = ("rating", "created_at")

@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "report_text", "created_at")
    search_fields = ("post__title", "user__email")
    list_filter = ("report_text", "created_at")

@admin.register(PostFile)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ("post", "file", "file_type", "created_at")
    search_fields = ("post__title", "file")
    list_filter = ("file_type", "created_at")


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "comment_text", "created_at")
    search_fields = ("post__title", "user__email", "comment_text")
    list_filter = ("created_at",)