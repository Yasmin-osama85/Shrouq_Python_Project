from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment

def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_body = request.POST.get('body')

            if comment_body:
                Comment.objects.create(
                    post=post,
                    author=request.user,
                    body=comment_body
                )

                return redirect('post_detail', post_id=post.id)

    return render(
        request,
        'posts/post_detail.html',
        {'post': post}
    )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    'posts/register.html',
                    {'error': 'Username already exists.'}
                )

            User.objects.create_user(
                username=username,
                password=password
            )

            return redirect('login')

    return render(request, 'posts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'posts/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'posts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
    
def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')

        if title and body:
            Post.objects.create(
                title=title,
                body=body,
                author=request.user
            )

            return redirect('home')

    return render(request, 'posts/add_post.html')    