from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostEdit, PostDelete
from .views import NewsCreate, ArticleCreate, NewsEdit, NewsDelete, ArticleEdit, ArticleDelete, NewsEdit, NewsDelete
from .views import CategoryListView, subscribe


urlpatterns = [
    path("", PostsList.as_view(), name='post_list'),
    path("<int:pk>", PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('news/create/', NewsCreate.as_view()),
    path('news/<int:pk>/edit/', NewsEdit.as_view()),
    path('news/<int:pk>/delete/', NewsDelete.as_view()),
    path('articles/create/', ArticleCreate.as_view()),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view()),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
    path("categories/<int:pk>", CategoryListView.as_view()),
    path("categories/<int:pk>/subscribe", subscribe),
]
