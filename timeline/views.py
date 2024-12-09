import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Comment, Post
from .forms import CommentForm, PostForm

@login_required(login_url='/accounts/login')
def main(request):
    query = request.GET.get('query')

    if query:
        posts = Post.objects.filter(text__contains=query).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'timeline.html', {
        'posts': posts,
        'user': request.user,
    })

@login_required(login_url='/accounts/login')
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            messages.success(request, "Your post has been successfully created!")
            return redirect('timeline:main')

    post_form = PostForm()

    return render(request, 'create_post.html', {
        'form': post_form,
    })

@login_required(login_url='/accounts/login')
def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'view_post.html', {
        'post': post,
        'comments': comments,
        'user': request.user,
    })

@login_required(login_url='/accounts/login')
def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=instance)

        if post_form.is_valid():
            post: Post = post_form.save(commit=False)
            post.is_edited = True
            post.save()

        return redirect('timeline:main')

    form = PostForm(instance=instance)
    return render(request, 'edit_post.html', {'form': form})

@login_required(login_url='/accounts/login')
def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        instance.delete()
        return redirect('timeline:main')

    return render(request, 'delete_post.html', {'post': instance})

@login_required(login_url='/accounts/login')
def get_posts(_):
    posts = Post.objects.all().order_by('-created_at')

    data = [
        {
            "id": post.id,
            "user": {
                "role": post.user.role,
                "display_name":
                    post.user.foodieprofile.full_name
                    if post.user.role == "Foodie" else
                    post.user.merchantprofile.restaurant_name,
                "username": post.user.username,
            },
            "text": post.text,
            "is_edited": post.is_edited,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        for post in posts
    ]

    return JsonResponse(data, content_type="application/json", safe=False)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def create_post_json(request):
    data = json.loads(request.body)

    post_form = PostForm(data)

    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.user = request.user
        post.save()

        return JsonResponse({
            "success": True,
            "message": "Posted!"
        }, status=200)

    return JsonResponse({
        "success": False,
        "errors": post_form.errors,
    }, status=200)

@login_required(login_url='/accounts/login')
def get_comments(_, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comments = [
        {
            'id': comment.id,
            'text': comment.text,
            'username': comment.user.username,
            'displayname': comment.user.foodieprofile.full_name if comment.user.role == 'Foodie' else comment.user.merchantprofile.restaurant_name,
            'user_role': comment.user.role,
            'user_id': comment.user.id,
            'is_edited': comment.is_edited,
        }
        for comment in Comment.objects.filter(post=post)
    ]

    return JsonResponse(comments, content_type="application/json", safe=False)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def create_comment(request, post_id):
    text = request.POST.get("text")
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    comment = Comment(user=user, post=post, text=text)
    comment.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/accounts/login')
def edit_comment(request, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, user=request.user)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=instance)

        if comment_form.is_valid():
            comment: Comment = comment_form.save(commit=False)
            comment.is_edited = True
            comment.save()

        return redirect('timeline:view_post', post_id=instance.post.id)

    form = CommentForm(instance=instance)
    return render(request, 'edit_comment.html', {
        'form': form,
        'comment': instance,
    })

@login_required(login_url='/accounts/login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('timeline:view_post', post_id=comment.post.id)

    return render(request, 'delete_comment.html', {'comment': comment, 'post': comment.post})
