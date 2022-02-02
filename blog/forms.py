from django import forms
from django.forms import fields
from .models import Post
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #авторизация и аутентификация
from django.contrib.auth.models import User
#from captcha.fields import CaptchaField, CaptchaTextInput


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}), help_text ='Введите свой логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}), help_text ='Введите свой пароль')
    #captcha = CaptchaField(widget=CaptchaTextInput)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #настройка в следующим виде работает некорректно
    '''
    widgets = {     
        'username': forms.TextInput(attrs={"class": "form-control"}),
        'email': forms.EmailInput(attrs={"class": "form-control"}),
        'password1': forms.PasswordInput(attrs={"class": "form-control"}),
        'password2': forms.PasswordInput(attrs={"class": "form-control"})
    }'''
    #тонкую настройку каждой формы можно осуществить следующим образом:
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    #captcha = CaptchaField(widget=CaptchaTextInput)
    
    class Meta:
        model = User    #связывает нашу модель с моделью User (from django.contrib.auth.models)
        fields = ('username', 'email', 'password1', 'password2')
        

#чтобы создать форму
class PostForm(forms.ModelForm):
    class Meta:
        model = Post    #атрибут model указывает с какой конкретно моделью связана наша форма
        #fields = '__all__'   
        #атрибут fields указывает какие поля мы хотим видеть в нашей форме. '__all__' - означает весь перечень полей
        # #полей is_published и update_at в отображении не будет, т.к.они заполняются автоматически
        fields = ['title', 'content', 'category', 'tags' ]  #лучше самостоятельно перечислить поля
        widgets = { 
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", 'rows': 5}),
            'category': forms.Select(attrs={"class": "form-control"}),
            'tags': forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):      #кастомный/пользовательский валидатор, self - объект данного класса
        title = self.cleaned_data['title']      #словарь с данными, где ключ 'title'
        if re.match(r'\d', title):   #поиск в строке title цифр. Используется бибилиотека regular expression
            raise ValidationError('Название не должно начинаться с цифры')       #возбуждение ошибки из библиотеки django.core.exception
        return title
