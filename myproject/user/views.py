from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import SignUpForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board.models import Post
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm




def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '회원가입에 성공했어요! 로그인 페이지로 이동합니다.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def mypage(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'user/mypage.html', {'posts':posts})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        pwd_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, '회원 정보가 변경되었어요.')
            return redirect('mypage')

        if pwd_form.is_valid():
            pwd_form.save()
            update_session_auth_hash(request, pwd_form.user)  # 세션 유지
            messages.success(request, '비밀번호가 변경되었어요.')
            return redirect('mypage')
    
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        pwd_form = PasswordChangeForm(request.user)

    return render(request, 'user/edit_profile.html', {
        'user_form' : user_form,
        'pwd_form' : pwd_form
    })