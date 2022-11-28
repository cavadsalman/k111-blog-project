from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout

# Create your views here.

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', context={'form': form})
    elif request.method == 'POST':
        nextURL = request.GET.get('next')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect(nextURL or 'info:home')
        else:
            return render(request, 'login.html', context={'form': form})
        
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', context={'form': form})
    elif request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('info:home')
        else:
            return render(request, 'register.html', context={'form': form})
    
        
def logout_view(request):
    logout(request)
    return redirect('user:login')
        
        
