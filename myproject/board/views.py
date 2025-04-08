from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, CommentLike
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form':form})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.user.is_authenticated:
        liked_comment_ids = set(
        CommentLike.objects.filter(user=request.user, comment__in=comments).values_list('comment_id', flat=True)
    )
    else:
        liked_comment_ids = set()

    for comment in comments:
        comment.is_liked = comment.id in liked_comment_ids


    is_liked = Like.objects.filter(post=post, user=request.user).exists if request.user.is_authenticated else False
    like_count = Like.objects.filter(post=post).count()

    if request.method=='POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.date_posted = timezone.now()
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post':post,
        'comments':comments,
        'form':form,
        'is_liked': is_liked,
        'like_count': like_count,
        
        })

def add_reply(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    parent_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.parent = parent_comment
            reply.save()
            return redirect('post_detail',pk=pk)
    else:
        form = CommentForm()

    return redirect('post_detail', pk=pk)

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post,pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post_detail', pk=pk)

@login_required
def toggle_comment_like(request, pk, comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        like.delete()

    return redirect('post_detail', pk=pk)