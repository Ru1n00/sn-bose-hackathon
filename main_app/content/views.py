from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from .utils import translate_text
from .models import (
    Post,
    PostFile,
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
    

def post_detail(request, slug):
    # Fetch the post by slug
    post = get_object_or_404(Post, slug=slug)


    # Fetch all files related to the post
    files = PostFile.objects.filter(post=post)
    images = files.filter(file_type__in=['jpg', 'jpeg', 'png'])
    videos = files.filter(file_type__in=['mp4', 'mkv'])

    lang = request.GET.get('lang', 'en')

    if lang == 'bn':
        # Translate the post title and description
        translated_title = translate_text(post.title)
        translated_description = translate_text(post.description)
        post.title = translated_title
        post.description = translated_description
        
    context = {
        'post': post,
        'videos': videos,
        'images': images,
    }
    return render(request, 'content/post_detail.html', context)
