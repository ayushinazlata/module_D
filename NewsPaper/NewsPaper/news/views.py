from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .forms import NewsForm
from .models import Post, Category, Author
from .filters import PostFilter

from datetime import datetime, timedelta, timezone
from django.utils import timezone

from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        limit = settings.DAY_LIMIT_POSTS
        today = timezone.now()
        prev_day = today - timedelta(hours=24)
        posts_day_count = Post.objects.filter(date_creation__gte=prev_day, author__authorUser=user).count()
        context['posts_limit'] = limit <= posts_day_count
        context['limit'] = limit
        context['count'] = posts_day_count
        context['date_creation'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class NewList(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.edit_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news'
    paginate_by = 10

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


@login_required
def subscribe(request, pk): # Подписка
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'You have successfully subscribed to the category news feed:'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def delete_subscribe(request, pk):  # Отписка
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'You have successfully unsubscribed from category news feed:'
    return render(request, 'delete_subscribe.html', {'category': category, 'message': message})


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(
                authorUser=User.objects.get(pk=user.id)
            )
    return redirect('news_list')
