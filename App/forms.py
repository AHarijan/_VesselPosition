from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'port', 'country')