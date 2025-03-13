from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Введите эл.почту'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Введите пароль'

    }))
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Введите эл.почту'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Введите пароль'

    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Подтвердите пароль'

    }))
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Устанавливаем хешированный пароль
        if commit:
            user.save()
        return user