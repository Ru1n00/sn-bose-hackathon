from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
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

from quiz.models import Quiz, QuizOption, QuizAnswer

from .forms import PostForm, PostFileFormSet

# Create your views here.
def index(request):
    return render(request, 'content/index.html')


# utility function to handle post creation and file uploads
def handle_post_creation(request, form):
    """Handles post creation and file uploads"""

    image_file = request.FILES.get("image_file")
    video_file = request.FILES.get("video_file")

    question = request.POST.getlist("questions[]")
    answer = request.POST.getlist("answers[]")
    option_a = request.POST.getlist("option_a[]")
    option_b = request.POST.getlist("option_b[]")
    option_c = request.POST.getlist("option_c[]")
    option_d = request.POST.getlist("option_d[]")

    is_quiz_posted = False

    if '' not in question and '' not in answer and '' not in option_a and '' not in option_b and '' not in option_c and '' not in option_d:
        is_quiz_posted = True
    
    if is_quiz_posted:
        # Check if the question and answer lists are of the same length
        if len(question) != len(answer):
            messages.error(request, "Question and answer lists must be of the same length.")
            return redirect("content:post_list")
        # Check if the options lists are of the same length
        if len(option_a) != len(option_b) or len(option_a) != len(option_c) or len(option_a) != len(option_d):
            messages.error(request, "Options lists must be of the same length.")
            return redirect("content:post_list")
        
        # Check if the question and options are not empty
        for q, a, op_a, op_b, op_c, op_d in zip(question, answer, option_a, option_b, option_c, option_d):
            if not q or not a or not op_a or not op_b or not op_c or not op_d:
                messages.error(request, "Question and options cannot be empty.")
                return redirect("content:post_list")
            
        # Check if the answer is one of the options
        for q, a, op_a, op_b, op_c, op_d in zip(question, answer, option_a, option_b, option_c, option_d):
            q = q.strip().lower()
            a = a.strip().lower()
            op_a = op_a.strip().lower()
            op_b = op_b.strip().lower()
            op_c = op_c.strip().lower()
            op_d = op_d.strip().lower()
            if a not in [op_a, op_b, op_c, op_d]:
                messages.error(request, "Answer must be one of the options.")
                return redirect("content:post_list")


    if form.is_valid():
        post = form.save(commit=False)
        post.post_user = request.user
        post.save()

        # Handle file uploads
        if image_file:
            PostFile.objects.create(post=post, file=image_file)
        if video_file:
            PostFile.objects.create(post=post, file=video_file)

        if is_quiz_posted:
            # Create quiz questions and options
            for q, a, op_a, op_b, op_c, op_d in zip(question, answer, option_a, option_b, option_c, option_d):
                # Create the quiz question
                quiz_question = Quiz.objects.create(post=post, question=q)

                # Create the quiz options
                QuizOption.objects.create(
                    quiz=quiz_question,
                    option_a=op_a,
                    option_b=op_b,
                    option_c=op_c,
                    option_d=op_d,
                    answer=a
                )

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
        Post.objects.select_related("category").prefetch_related("postfile_set", "postcomment_set", "quiz_set__quizoption_set", "quiz_set__quizanswer_set").order_by("-created_at"),
        slug=slug)


    # check if answers are already submitted
    user_has_taken_quiz = QuizAnswer.objects.filter(user=request.user, quiz__post=post).exists()

    # Calculate total score efficiently
    quiz_answers = QuizAnswer.objects.filter(user=request.user, quiz__post=post).aggregate(
        correct_count=Count("id", filter=Q(is_correct=True))
    )

    total_score = quiz_answers["correct_count"] * 10

    full_mark = len(Quiz.objects.filter(post=post)) * 10

    user_answers = QuizAnswer.objects.filter(user=request.user, quiz__post=post).select_related("quiz")

    lang = request.GET.get('lang', 'en')

    if lang == 'bn':
        # Translate the post title and description
        translated_title = translate_text(post.title)
        translated_description = translate_text(post.description)
        post.title = translated_title
        post.description = translated_description

    context = {
        'post': post,
        'user_has_taken_quiz': user_has_taken_quiz,
        'total_score': total_score,
        'full_mark': full_mark,
        'user_answers': user_answers,
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

        # update user streak
        user_profile = request.user.contentuserprofile
        user_profile.update_streak()

        messages.success(request, "Comment added successfully!")
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
