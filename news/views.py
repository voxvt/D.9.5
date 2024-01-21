from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Category, CategorySubscribe, PostCategory
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string


class PostsList(ListView):

    model = Post
    ordering = "-created_at"

    template_name = "news.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)

        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):

    model = Post
    template_name = "new.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()

        return context

class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):

    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.add_post')

class PostSearch(ListView):

        model = Post
        ordering = '-created_at'
        template_name = 'post_search.html'
        context_object_name = 'posts_search'
        paginate_by = 10

        def get_queryset(self):
            queryset = super().get_queryset()
            self.filterset = PostFilter(self.request.GET, queryset=queryset)

            return self.filterset.qs

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['filterset'] = self.filterset
            return context

class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.change_post')

class PostDelete(PermissionRequiredMixin, DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post')

class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.add_post')

    def form_valid(self, form):
        form.instance.post_type = 'новость'
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.add_post')

    def form_valid(self, form):
        form.instance.post_type = 'статья'
        return super().form_valid(form)

class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post  # Замените на вашу модель статьи
    fields = ['author', 'post_category', 'post_title', 'post_text']  # Укажите поля, которые нужно редактировать
    template_name = 'article_edit.html'  # Укажите имя вашего шаблона
    permission_required = ('news.change_post')

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post  # Замените на вашу модель статьи
    success_url = reverse_lazy('post_list')  # Укажите адрес после успешного удаления
    permission_required = ('news.delete_post')

class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post  # Замените на вашу модель новости
    fields = ['author', 'post_category', 'post_title', 'post_text']  # Укажите поля, которые нужно редактировать
    template_name = 'news_edit.html'  # Укажите имя вашего шаблона
    permission_required = ('news.change_post')

class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post  # Замените на вашу модель новости
    success_url = reverse_lazy('post_list')  # Укажите адрес после успешного удаления
    permission_required = ('news.delete_post')

class CategoriesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'categories.html', {'categories' : Category.objects.all()})

class CategoryDetail(LoginRequiredMixin, DetailView):

    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribed.html')

# Create your views here.
def notify_new_post_in_category(instance, **kwargs):

    category_id = instance.post_category.id

    subscribed_users = []
    subscribed_users_1 = CategorySubscribe.objects.filter(category_id=int(category_id))

    for user in subscribed_users_1:
        subscribed_users.append(User.objects.get(id=user.subscriber_id).email)

    print(subscribed_users)

    send_mail(
        subject=f'Новый пост в категории {Category.objects.get(id=category_id)}',
        html_message=render_to_string('new_post.html',
        context={'post' : instance, 'category' : Category.objects.get(id=category_id).category_name,
                'link' : f'http://127.0.0.1:8000/{instance.id}'}),
        message='',
        from_email='ruslanSkillFactory@yandex.ru',
        recipient_list=subscribed_users
    )

post_save.connect(notify_new_post_in_category, sender=Post)