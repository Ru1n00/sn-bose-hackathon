from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, FormView
from django.contrib import messages

from .utils import translate_text
from .models import (
    Post,
    PostFile,
    PostComment,
    Category,
)

from .forms import PostForm, PostFileFormSet

# Create your views here.
def index(request):
    return render(request, 'content/index.html')


# utility function to handle post creation and file uploads
def handle_post_creation(request, form):
    """Handles post creation and file uploads"""

    image_file = request.FILES.get("image_file")
    video_file = request.FILES.get("video_file")

    if form.is_valid():
        post = form.save(commit=False)
        post.post_user = request.user
        post.save()

        # Handle file uploads
        if image_file:
            PostFile.objects.create(post=post, file=image_file)
        if video_file:
            PostFile.objects.create(post=post, file=video_file)

        messages.success(request, "Post created successfully!")
        return redirect("content:post_list")  # Redirect after successful submission
    else:
        messages.error(request, "Error creating post. Please check the form.")
        return None  # Indicate form errors

class PostListView(LoginRequiredMixin, ListView, FormView):
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Number of posts per page
    form_class = PostForm

    def get_queryset(self):
        self.category = self.request.user.contentuserprofile.favorite_subject
        # posts = Post.objects.filter(category=self.category, is_active=True).select_related("category").order_by("-created_at")
        posts = Post.objects.filter(category=self.category, is_active=True).select_related("category").prefetch_related("postfile_set").order_by("-created_at")
        
        if not posts.exists():
            # If no posts in the user's favorite category, fetch all active posts
            posts = Post.objects.filter(is_active=True).select_related("category").prefetch_related("postfile_set").order_by("-created_at")
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["form"] = self.get_form(self.form_class)
        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        result = handle_post_creation(request, form)
        return result if result else self.get(request, *args, **kwargs)
    
    
class CategoryPostListView(LoginRequiredMixin, ListView, FormView):
    model = Post
    template_name = "content/post_list.html"
    context_object_name = "posts"
    form_class = PostForm

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
        return Post.objects.filter(category=self.category, is_active=True).select_related("category").prefetch_related("postfile_set").order_by("-created_at")

    def get_context_data(self, **kwargs):
        """ Pass category to context without redundant query """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category  # Use the category already fetched in `get_queryset()`
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        result = handle_post_creation(request, form)
        return result if result else self.get(request, *args, **kwargs)


class PostSearchView(LoginRequiredMixin, ListView, FormView):
    model = Post
    template_name = "content/post_search_results.html"
    context_object_name = "posts"
    form_class = PostForm

    def get_queryset(self):
        query = self.request.GET.get("q")  # Get search query from URL
        if query:
            return Post.objects.filter(is_active=True).filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).select_related("category").prefetch_related("postfile_set").order_by("-created_at")
        return Post.objects.none()  # Return empty queryset if no query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        result = handle_post_creation(request, form)
        return result if result else self.get(request, *args, **kwargs)


@login_required
def post_detail(request, slug):
    # Fetch the post by slug

    post = get_object_or_404(
        Post.objects.select_related("category").prefetch_related("postfile_set", "postcomment_set").order_by("-created_at"),
        slug=slug)


    lang = request.GET.get('lang', 'en')

    if lang == 'bn':
        # Translate the post title and description
        translated_title = translate_text(post.title)
        translated_description = translate_text(post.description)
        post.title = translated_title
        post.description = translated_description

    context = {
        'post': post,
    }
    return render(request, 'content/post_detail.html', context)

@login_required
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

@login_required
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


@login_required
def make_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment_text = request.POST.get("comment_text")
        comment_parent_id = request.POST.get("comment_parent_id")

        if not post_id or not comment_text:
            messages.error(request, "comment text are required.")
            return redirect("content:post_detail", slug=post.slug)
        
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Create a new comment
        comment = PostComment.objects.create(
            post=post,
            user=user,
            comment_text=comment_text,
            comment_parent_id=comment_parent_id if comment_parent_id else None,
        )

        return redirect("content:post_detail", slug=post.slug)
    

@login_required
def post_upvote(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.upvotes += 1
    post.save()
    return redirect("content:post_detail", slug=post.slug)


@login_required
def post_downvote(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.downvotes += 1
    post.save()
    return redirect("content:post_detail", slug=post.slug)
