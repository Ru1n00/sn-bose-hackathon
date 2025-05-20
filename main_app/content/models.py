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

