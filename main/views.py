from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import RegistrationForm, CreatePostForm, EditProfileForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.db.models import Count
from main.models import Post, MyUser, Comment
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse
from .forms import EditPostForm


def index(request):
    return render(request, 'basic.html')


class MainLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse('main:index')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:index')


@login_required
def profile(request):
    user_posts = Post.objects.filter(MyUser=request.user).order_by('-pub_date').annotate(
        comment_count=Count('comment'),
        like_count=Count('likes')
    )

    context = {
        'post_list': user_posts,
    }
    return render(request, 'profile.html', context)

class EditProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MyUser
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные изменены'

    def get_object(self, queryset=None):
        return self.request.user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = MyUser
    template_name = 'delete_profile.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.MyUser = request.user
            Post.pub_date = timezone.now()
            Post.save()
            return redirect('main:index')
    else:
        form = CreatePostForm()
    return render(request, 'create_post.html', {'form': form, })

class PostListView(generic.ListView):
    model = Post
    paginate_by = 3
    template_name = 'index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:50].annotate(
            comment_count=Count('comment'),
            like_count=Count('likes')
        )


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.MyUser != request.user:
        return redirect('main:index')

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:index'))
        else:
            return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        form = EditPostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('main:index')
    template_name = "delete_post.html"

    def test_func(self):
        obj = self.get_object()
        return obj.MyUser == self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.image:
            self.object.image.delete(save=False)
        return super().delete(request, *args, **kwargs)


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get('comment_text')
            Comment.objects.create(
                post=post,
                comment_text=comment_text if comment_text else '',
                my_user=request.user
            )
            return redirect('main:index')
        else:
            pass
    else:
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'add_comment.html', context)


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.my_user:
        return redirect('main:index')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.comment_text = form.cleaned_data['comment_text']
            comment.save()
            return redirect('main:index')
    else:
        form = CommentForm(initial={'comment_text': comment.comment_text})

    context = {'form': form, 'comment': comment}
    return render(request, 'edit_comment.html', context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.my_user:
        return redirect('main:index')

    if request.method == 'POST':
        comment.delete()
        return redirect('main:index')

    return redirect('main:index')

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('main:index')