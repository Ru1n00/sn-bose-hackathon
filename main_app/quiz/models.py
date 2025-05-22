from django.db import models

from accounts.models import CustomUser
from content.models import Post


# Create your models here.
class Quiz(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question
    

class QuizOption(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer
    

    def save(self, *args, **kwargs):
        # Ensure that the answer is one of the options
        self.option_a = self.option_a.strip().lower()
        self.option_b = self.option_b.strip().lower()
        self.option_c = self.option_c.strip().lower()
        self.option_d = self.option_d.strip().lower()
        self.answer = self.answer.strip().lower()

        if self.answer not in [self.option_a, self.option_b, self.option_c, self.option_d]:
            raise ValueError("Answer must be one of the options.")
        super().save(*args, **kwargs)


class QuizAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.selected_option}"