from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Новости'    #меянет заголовок в админке с News на "Новости" 

    def ready(self):
        import blog.signals     #импортирование сигналов