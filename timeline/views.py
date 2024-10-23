from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

def main(request):
    posts = Post.objects.all()
    return render(request, 'timeline.html', {'posts':posts})

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
