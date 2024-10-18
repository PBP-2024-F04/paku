from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
