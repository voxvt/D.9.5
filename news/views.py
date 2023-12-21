from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post, Comment


class PostsList(ListView):

    model = Post
    ordering = "-created_at"

    template_name = "news.html"
    context_object_name = "posts"


    Post.objects.all()

class PostDetail(DetailView):

    model = Post
    template_name = "new.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()

        return context


