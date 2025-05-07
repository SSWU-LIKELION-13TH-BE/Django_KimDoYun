from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import SignUpForm, CustomUserChangeForm, GuestBookForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board.models import Post
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import GuestBook, CustomUser
from django.contrib.auth.models import User


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

@login_required
def guestbook_list(request, username):
    owner = get_object_or_404(CustomUser, username=username)
    guestbooks = GuestBook.objects.filter(owner=owner).order_by('-created_at')
    return render(request, 'user/guestbook_list.html', {'owner': owner, 'guestbooks': guestbooks})

@login_required
def guestbook_write(request, username):
    owner = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        form = GuestBookForm(request.POST)
        if form.is_valid():
            GuestBook.objects.create(
                owner=owner,
                writer=request.user,
                content=form.cleaned_data['content']  
            )
            return redirect('guestbook_write', username=username)
    else:
        form = GuestBookForm()

    return render(request, 'user/guestbook_write.html', {'form': form, 'owner': owner})

@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'user/user_list.html', {'users':users})