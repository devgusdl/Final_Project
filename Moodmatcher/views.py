# Moodmatcher/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, CommentForm, PostUpdateForm, CommentForm, ImageUploadForm
from .models import Post, Comment, Profile, PostLike


def main_page(request):
    return render(request, 'Moodmatcher/main.html')

def service_intro(request):
    return render(request, 'Moodmatcher/service_intro.html')

def recommend_view(request):
    return render(request, 'Moodmatcher/recommend_overview.html')

def image_choice_recommend(request):
    return render(request, 'Moodmatcher/image_choice_recommend.html')

@login_required(login_url='/login/')
def image_upload_recommend(request):
    if not request.user.is_authenticated:
        messages.warning(request, "이미지 업로드 기반 추천 서비스는 회원 전용 서비스입니다. 로그인 후 이용해주세요.")
        return redirect('login')

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "이미지 업로드가 성공적으로 완료되었습니다.")
            return redirect('recommendations') 
        else:
            messages.error(request, "이미지 업로드에 실패하였습니다. 다시 시도해주세요.")
    else:
        form = ImageUploadForm()

    return render(request, 'Moodmatcher/image_upload_recommend.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'Moodmatcher/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.error(request, "아이디나 비밀번호가 일치하지 않습니다.")
    else:
        form = AuthenticationForm()
    return render(request, 'Moodmatcher/login.html', {'form': form})

@login_required(login_url='/login/')
def community(request):
    posts = Post.objects.filter(category='community').order_by('-created_at')
    return render(request, 'Moodmatcher/community.html', {'posts': posts})

def customer_service(request):
    posts = Post.objects.filter(category='customer-service').order_by('-created_at')
    return render(request, 'Moodmatcher/customer_service.html', {'posts': posts})

def post_detail(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    post.views += 1
    post.save()

    return render(request, 'Moodmatcher/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'category': category})

@login_required(login_url='/login/')
def post_create(request, category):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category
            post.save()
            return redirect('community' if category == 'community' else 'customer_service')
    else:
        form = PostForm()
    return render(request, 'Moodmatcher/post_create.html', {'form': form, 'category': category})

@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, '댓글이 성공적으로 작성되었습니다.')
    return redirect('post_detail', category=post.category, post_id=post.id)

@login_required(login_url='/login/')
def post_update(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category, author=request.user)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect('post_detail', category=category, post_id=post_id)
    else:
        form = PostUpdateForm(instance=post)
    return render(request, 'Moodmatcher/post_update.html', {'form': form, 'category': category, 'post_id': post_id})

@login_required(login_url='/login/')
def post_delete(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
        return redirect('community' if category == 'community' else 'customer_service')
    return render(request, 'Moodmatcher/post_delete.html', {'post': post, 'category': category})

@login_required(login_url='/login/')
def post_create_customer_service(request, category):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category
            post.save()
            return redirect('customer_service')
    else:
        form = PostForm()
    return render(request, 'Moodmatcher/post_create_customer_service.html', {'form': form, 'category': category})

@login_required(login_url='/login/')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', category=comment.post.category, post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'Moodmatcher/comment_update.html', {'form': form, 'comment': comment})


@login_required(login_url='/login/')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        messages.success(request, '댓글이 성공적으로 삭제되었습니다.')
        return redirect('post_detail', category=comment.post.category, post_id=comment.post.id)
    return render(request, 'Moodmatcher/comment_delete.html', {'comment': comment})



@login_required
def my_profile(request):
    # 현재 로그인한 사용자의 댓글과 게시글을 가져오기
    user = request.user
    comments = Comment.objects.filter(author=user)
    posts = Post.objects.filter(author=user)

    # 현재 사용자가 좋아요를 누른 게시물을 가져오기
    liked_posts = request.user.post_likes.all()

    # 모든 게시물 가져오기
    all_posts = Post.objects.all()

    # 좋아요한 게시물 객체 가져오기
    liked_post_objects = Post.objects.filter(id__in=liked_posts)

    # 사용자 프로필 가져오기
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile,
        'comments': comments,
        'posts': posts,
        'liked_posts': liked_post_objects,  # 여기에 좋아요한 게시물 포함
    }

    return render(request, 'Moodmatcher/my_profile.html', context)



@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 좋아요 토글 로직: 이미 좋아요를 누른 경우 제거, 아니면 추가
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    # 현재 사용자가 좋아요를 누른 게시물을 가져오기
    liked_posts = request.user.post_likes.all()

    # 모든 게시물 가져오기
    all_posts = Post.objects.all()

    # 사용자에게 반환할 데이터
    return render(request, 'Moodmatcher/post_detail.html', {'post': post, 'category': post.category, 'liked_posts': liked_posts, 'all_posts': all_posts})