from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from .utils import translate_text
from .models import (
    Post,
    PostFile,
)

from .forms import PostForm, PostFileFormSet

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


def post_create(request):
    if request.method == 'POST':
        # Handle form submission
        form = PostForm(request.POST)

        # Handle file uploads
        file_form = PostFileFormSet(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_user = request.user
            post.save()
            # Handle file uploads
            file_form = PostFileFormSet(request.POST, request.FILES, instance=post)

            for form in file_form:
                if form.is_valid():
                    if form.cleaned_data.get('file'):
                        post_file = form.save(commit=False)
                        post_file.post = post

                        post_file.save()
            return redirect('content:post_list')
    else:
        form = PostForm()
        # Handle file uploads
        file_form = PostFileFormSet()

    return render(request, 'content/post_create.html', {'form': form, 'file_form': file_form})


def post_edit(request, slug):
    # Fetch the post by slug
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        # Handle form submission
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_user = request.user
            post.save()
            # Handle file uploads
            file_form = PostFileFormSet(request.POST, request.FILES, instance=post)
            for form in file_form:
                if form.is_valid():
                    if form.cleaned_data.get('file'):
                        post_file = form.save(commit=False)
                        post_file.post = post
                        post_file.save()
            return redirect('content:post_list')
    else:
        form = PostForm(instance=post)
        file_form = PostFileFormSet(instance=post)

    return render(request, 'content/post_edit.html', {'form': form, 'file_form': file_form})
