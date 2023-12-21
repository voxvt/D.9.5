from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        from .models import Post, Comment

        # Обновление и расчёт рейтинга
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(posts_rating_sum =Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(comments_rating_sum = Sum('comment_rating'))

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()

class Category(models.Model):


    category_name = models.CharField(max_length=25, unique=True)  # Название категории

    def __str__(self):
        return self.category_name


class Post(models.Model):

    # Содержит в себе статьи/новости

    ART = 'С'
    NEWS = 'Н'

    TYPES = [(ART, 'Статья'), (NEWS, 'Новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    post_type = models.CharField(max_length=10, choices=TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    post_category = models.ManyToManyField(Category)

    post_title = models.CharField(max_length=120)

    post_text = models.TextField()

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
        return f'{self.post_title} : {self.post_text[:20]}'


class PostCategory(models.Model):

    category_PostCategory = models.ManyToManyField(Category)
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_text = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()


    def dislike(self):
        self.comment_rating -= 1
        self.save()





