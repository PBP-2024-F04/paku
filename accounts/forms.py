from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import FoodieProfile, MerchantProfile, User

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']

class FoodieProfileForm(forms.ModelForm):
    class Meta:
        model = FoodieProfile
        fields = ['full_name']

class MerchantProfileForm(forms.ModelForm):
    class Meta:
        model = MerchantProfile
        fields = ['restaurant_name']
