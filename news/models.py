from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.template.backends import django
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):

    # Модель содержащая объекты всех авторов

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ID пользователя, который является автором
    author_rating = models.IntegerField(default=0)

    def update_rating(self):

        # Обновление и расчёт рейтинга
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(posts_rating_sum =Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(comments_rating_sum = Sum('comment_rating'))

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):

    # Категории новостей/статей

    name = models.CharField(max_length=25, unique=True)  # Название категории
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class CategorySubscribe(models.Model):

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subscriber = models.ForeignKey(User, on_delete=models.PROTECT)


class Post(models.Model):

    # Содержит в себе статьи/новости

    ART = 'С'
    NEWS = 'Н'

    TYPES = [(ART, 'Статья'), (NEWS, 'Новость')]

    # ID автора поста
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Тип поста (статья/новость)
    post_type = models.CharField(max_length=10, choices=TYPES)
    # Дата и время создания поста
    created_at = models.DateTimeField(auto_now_add=True)
    # Категория поста
    post_category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    # Заголовок статьи/новости
    post_title = models.CharField(max_length=120)
    # Текст статьи/новости
    post_text = models.TextField()
    # Рейтинг статьи/новости
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()


    def dislike(self):
        self.post_rating -= 1
        self.save()


    def preview(self):
        return self.post_text[:125] + '...'


    def __str__(self):
        return f'{self.post_title} : {self.post_text[:20]} : {self.post_category}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):

    # Промежуточная модель для связи "многие ко многим"

    category_PostCategory = models.ManyToManyField(Category)
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):

    # Комментарии к постам

    # ID поста
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ID пользователя, оставившего комментарий
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    comment_text = models.CharField(max_length=255)
    # Время создания комментария
    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()


    def dislike(self):
        self.comment_rating -= 1
        self.save()
