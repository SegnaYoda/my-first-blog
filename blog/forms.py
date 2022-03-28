from django import forms
from django.forms import Textarea, fields
from .models import Post, Comment, UserProfile
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #авторизация и аутентификация
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}), help_text ='Введите свой логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}), help_text ='Введите свой пароль')
    captcha = CaptchaField(widget=CaptchaTextInput)


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
    username = forms.CharField(label='Имя пользователя(Логин)', widget=forms.TextInput(attrs={"class": "form-control"}), help_text ='Логин необходим для авторизации на сайте')
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    #avatar  = forms.ImageField(label='Загрузите свой аватар',)
    #author = forms.CharField(label='Псевдоним', widget=forms.TextInput(attrs={"class": "form-control"}))
    #discription = forms.CharField(label='О себе', required=False, widget=forms.Textarea(attrs={
    #  "class": "form-control",
    #  "rows": 5
    #  }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = CaptchaField(widget=CaptchaTextInput, help_text ='Введите текст на изображении')

    class Meta:
        model = User    #связывает нашу модель с моделью User (from django.contrib.auth.models)
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



    def clean_title(self):      #кастомный/пользовательский валидатор, self - объект данного класса
        title = self.cleaned_data['title']      #словарь с данными, где ключ 'title'
        if re.match(r'\d', title):   #поиск в строке title цифр. Используется бибилиотека regular expression
            raise ValidationError('Название не должно начинаться с цифры')       #возбуждение ошибки из библиотеки django.core.exception
        return title


class CommentForm(forms.ModelForm):  
    class Meta:  
       model = Comment  
       fields = ['body', ]  #лучше самостоятельно перечислить поля
       widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", 'rows': 5, 'placeholder' : "Комментарий", 'message' : "message"}, ),
            #'title': forms.TextInput(attrs={"class": "form-control"}),
            #'category': forms.Select(attrs={"class": "form-control"})
        }
       labels = {
            'body': '',}
       #help_texts = {
        #    'body': 'Количество символов ограничено 400 знаков.',}
       error_messages = {
            'body': {
                'max_length': "Количество символов превышает 400 знаков.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #for field in self.fields:
        #    self.fields[field].widget.attrs['class'] = 'form-control'
        #self.fields['body'].widget = Textarea(attrs={'row': 5})



    '''
    def clean_title(self):      #кастомный/пользовательский валидатор, self - объект данного класса
        title = self.cleaned_data['title']      #словарь с данными, где ключ 'title'
        if re.match(r'\d', title):   #поиск в строке title цифр. Используется бибилиотека regular expression
            raise ValidationError('Название не должно начинаться с цифры')       #возбуждение ошибки из библиотеки django.core.exception
        return title
    '''



class PostForm(forms.ModelForm):
    prepopulated_fields = {"slug": ("title",)}
    title = forms.CharField(label='Название новости', widget=forms.TextInput(attrs={"class": "form-control", "help_text" :'Введите название статьи', "autocomplete":"off"}))
    #photo = forms.ImageField(label='Загрузите свое фото',)
    content = forms.CharField(widget=CKEditorWidget, label='Содержание')
    class Meta:
        model = Post    #атрибут model указывает с какой конкретно моделью связана наша форма
        #fields = '__all__'
        #атрибут fields указывает какие поля мы хотим видеть в нашей форме. '__all__' - означает весь перечень полей
        # #полей is_published и update_at в отображении не будет, т.к.они заполняются автоматически
        fields = ['title', 'photo', 'category', 'tags', 'content', 'is_published' ]  #лучше самостоятельно перечислить поля
        widgets = {
            'category': forms.Select(attrs={"class": "form-control"}),
            'photo': forms.FileInput(attrs={"class": "form-control"}),
            'tags': forms.SelectMultiple(attrs={"enctype": "multipart/form-data", "type":"file"}),
            #'author': forms.Select(attrs={"class": "form-control"}),
            'is_published' : forms.CheckboxInput(),
        }
    

class PostEditForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget, label='ContenT')
    #photo = forms.ImageField(label='Загрузите свое фото',)
    

                                  