from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import UserAuthenticationForm


# Create your views here.
def sign_in(request):
    # messages.info(request, "Please log in to your account.")
    if request.user.is_authenticated:
        return redirect('content:index')  # Redirect to home if already authenticated
    
    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST)
        print(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'content/index.html', {'user': user})
            else:
                messages.error(request, "Invalid email or password.")
                return render(request, 'accounts/sign_in.html', {'form': form})
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'accounts/sign_in.html', {'form': form})
    else:
        form = UserAuthenticationForm()
    return render(request, 'accounts/sign_in.html', {'form': form})
