from django import forms 
from . models import UserPersonalModel, UserPredictModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserPersonalForm(forms.ModelForm):
    
    class Meta:
        model = UserPersonalModel
        fields = '__all__'


class UserPredictForm(forms.ModelForm):
    class Meta:
        model = UserPredictModel
        fields = ['text']

