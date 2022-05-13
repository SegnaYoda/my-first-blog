from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = 'Чаты'    #меняет заголовок в админке с News на "Новости" 

    def ready(self):
        import blog.signals     #импортирование сигналов