from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import is_valid_path
from urllib.parse import urlparse

from .forms import UserAuthenticationForm


# Create your views here.
def sign_in(request):
    # messages.info(request, "Please log in to your account.")
    if request.user.is_authenticated:
        return redirect('content:index')  # Redirect to home if already authenticated
    
    next_url = request.GET.get("next", "")

    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            next_url = request.POST.get('next', '')
            if user is not None:
                login(request, user)
                # Ensure next_url is safe or default to home page
                parsed_url = urlparse(next_url)
                if not parsed_url.netloc and is_valid_path(next_url):
                    return redirect(next_url)
                else:
                    return render(request, 'content/index.html', {'user': user})
            else:
                messages.error(request, "Invalid email or password.")
                return render(request, 'accounts/sign_in.html', {'form': form, 'next': next_url})
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'accounts/sign_in.html', {'form': form, 'next': next_url})
    else:
        form = UserAuthenticationForm()
    return render(request, 'accounts/sign_in.html', {'form': form, 'next': next_url})
