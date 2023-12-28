from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

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

class PostCreate(CreateView):

    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

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

class PostEdit(UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.post_type = 'новость'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.post_type = 'статья'
        return super().form_valid(form)

class ArticleEdit(UpdateView):
    model = Post  # Замените на вашу модель статьи
    fields = ['author', 'post_category', 'post_title', 'post_text']  # Укажите поля, которые нужно редактировать
    template_name = 'article_edit.html'  # Укажите имя вашего шаблона

class ArticleDelete(DeleteView):
    model = Post  # Замените на вашу модель статьи
    success_url = reverse_lazy('post_list')  # Укажите адрес после успешного удаления

class NewsEdit(UpdateView):
    model = Post  # Замените на вашу модель новости
    fields = ['author', 'post_category', 'post_title', 'post_text']  # Укажите поля, которые нужно редактировать
    template_name = 'news_edit.html'  # Укажите имя вашего шаблона

class NewsDelete(DeleteView):
    model = Post  # Замените на вашу модель новости
    success_url = reverse_lazy('post_list')  # Укажите адрес после успешного удаления

