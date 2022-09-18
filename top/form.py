from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "is_employer", "password1", "password2"]