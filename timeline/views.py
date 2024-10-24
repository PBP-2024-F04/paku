from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Comment, Post
from .forms import PostForm

def main(request):
    posts = Post.objects.all()
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

def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'view_post.html', {'post': post, 'comments': comments})

def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=instance)

        if post_form.is_valid():
            post_form.save()

        return redirect('timeline:main')

    form = PostForm(instance=instance)
    return render(request, 'edit_post.html', {'form': form})

def delete_post(request, post_id):
    return render(request, 'delete_post.html', {'post_id':post_id})

def get_comments(_, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comments = [
        {
            'text': comment.text,
            'username': comment.user.username,
            'user_fullname': comment.user.foodieprofile.full_name,
        }
        for comment in Comment.objects.filter(post=post)
    ]

    return JsonResponse(list(comments), safe=False)

@csrf_exempt
@require_POST
def create_comment(request, post_id):
    text = request.POST.get("text")
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    comment = Comment(user=user, post=post, text=text)
    comment.save()

    return HttpResponse(b"CREATED", status=201)

