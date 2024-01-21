from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'


    def ready(self):
        from.tasks import send_weekly
        from .scheduler import posts_scheduler

        posts_scheduler.add_job(
            id='send weekly',
            func=send_weekly,
            trigger='interval',
            weeks=1,
        )

        posts_scheduler.start()