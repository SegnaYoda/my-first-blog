from django.db.models.signals import post_save  # сигналы событий
from django.dispatch import receiver    #декоратор 
from django.contrib.auth.models import User
from .models import UserProfile


#использование библиотеки сигналов для отслеживания событий
@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):    #проверка, в случае создания нового пользователя создается профиль этого пользователя UserProfile
    if created:
        UserProfile.objects.create(user=instance)
        print(f'Профиль пользователя {instance} добавлен')
#post_save.connect(create_userprofile, sender=User)  
# вызов функции create_userprofile, этот способ можно заменить декоратором @receiver(post_save, sender=User)

@receiver(post_save, sender=User)
def update_userprofile(sender, instance, created, **kwargs):   #проверка, в случае обновления данных пользователя профиль этого пользователя обновляется 
    if created == False:
        instance.userprofile.save()
        print(f'Профиль пользователя {instance} обновлен')
#post_save.connect(update_userprofile, sender=User) 

#чтобы этот код работал необходимо прописать импорт в apps.py
