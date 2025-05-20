from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser


# Category Model
class Category(models.Model):
    # choices=[
    #     ('physics', 'Physics'),
    #     ('chemistry', 'Chemistry'),
    #     ('math', 'Math'),
    #     ('biology', 'Biology'),
    #     ('tech', 'Tech'),
    #     ('innovation', 'Innovation'),
    #     ('research', 'Research'),
    #     ('engineering', 'Engineering'),
    # ]
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


# Custom User Model
class ContentUserProfile(CustomUser):
    full_name = models.CharField(max_length=255)
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)

    STAGE_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('higher_secondary', 'Higher Secondary'),
        ('undergrad', 'Undergraduate'),
        ('grad', 'Graduate'),
        ('phd', 'PhD'),
    ]
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True)

    favorite_subject = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)


# Post Model
class Post(models.Model):
    post_user = models.ForeignKey(ContentUserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    stage = models.CharField(max_length=20, choices=ContentUserProfile.STAGE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    # rating
    def get_rating(self):
        ratings = PostRating.objects.filter(post=self)
        if ratings.exists():
            return sum(rating.rating for rating in ratings) // ratings.count()
        return 0
    

# Post Rating Model
class PostRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(ContentUserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f'{i}/5 Stars') for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')  # Composite Key

# Post Report Model
class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(ContentUserProfile, on_delete=models.CASCADE)
    REPORT_CHOICES = [
        ('misinformation', 'Misinformation'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('others', 'Others'),
    ]
    report_text = models.CharField(max_length=50, choices=REPORT_CHOICES)
    report_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')  # Composite Key


# File Model
class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='post_files/')
    file_type = models.CharField(max_length=10, editable=False)  # Store file extension
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = self.file.name.split('.')[-1]  # Extract file extension
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Comment Model
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(ContentUserProfile, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)