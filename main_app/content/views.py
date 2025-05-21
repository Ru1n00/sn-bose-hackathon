from django.shortcuts import render
from django.views.generic import ListView

from .models import (
    Post
)

# Create your views here.
def index(request):
    return render(request, 'content/index.html')

class PostListView(ListView):
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context