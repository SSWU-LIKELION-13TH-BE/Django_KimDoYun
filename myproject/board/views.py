from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, CommentLike
from .forms import PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form':form})

def post_list(request):
    sort = request.GET.get('sort', 'recent')  # 기본은 'recent'
    if sort == 'popular':
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-created_at')  # 인기순 (like_count 기준)
    else:
        posts = Post.objects.all().order_by('-created_at')  # 최신순 (created_at 기준)

    return render(request, 'post_list.html', {'posts': posts, 'sort': sort})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    post.view_count += 1  # 조회수 증가
    post.save()  # 변경사항 저장

    # 댓글 좋아요 상태 확인
    if request.user.is_authenticated:
        liked_comment_ids = set(
        CommentLike.objects.filter(user=request.user, comment__in=comments).values_list('comment_id', flat=True)
    )
    else:
        liked_comment_ids = set()

    for comment in comments:
        comment.is_liked = comment.id in liked_comment_ids

    #게시물 좋아요 상태 확인
    is_liked = Like.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False
    like_count = Like.objects.filter(post=post).count()

    #댓글 작성 폼 렌더링
    form = CommentForm()

    return render(request, 'post_detail.html', {
        'post':post,
        'comments':comments,
        'form':form,
        'is_liked': is_liked,
        'like_count': like_count,
        
        })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.date_posted = timezone.now()
            comment.save()
            return redirect('board:post_detail', pk=post.pk)  
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'form': form})


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
            return redirect('board:post_detail',pk=pk)
    else:
        form = CommentForm()

    return redirect('board:post_detail', pk=pk)

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post,pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('board:post_detail', pk=pk)

@login_required
def toggle_comment_like(request, pk, comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        like.delete()

    return redirect('board:post_detail', pk=pk)

def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(title__icontains=query)

    return render(request, 'search.html', {
        'form': form,
        'query': query,
        'results': results,
    })

def mypage(request):
    return render(request, 'user/mypage.html')

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form':form, 'post':post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('board:post_list')
    return render(request, 'board/post_delete.html', {'post':post})