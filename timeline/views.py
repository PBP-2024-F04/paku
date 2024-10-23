from django.contrib import messages
from django.shortcuts import redirect, render
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
    return render(request, 'edit_post.html', {'post_id':post_id})

def delete_post(request, post_id):
    return render(request, 'delete_post.html', {'post_id':post_id})
