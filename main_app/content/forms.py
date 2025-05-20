from django import forms
from django.forms import inlineformset_factory

from .models import Post, PostFile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'stage']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }



class PostFileForm(forms.ModelForm):
    class Meta:
        model = PostFile
        fields = ['file']


PostFileFormSet = inlineformset_factory(Post, PostFile, form=PostFileForm, extra=1, can_delete=True)
