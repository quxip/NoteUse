# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User

# class UserRegisterForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User 
#         fields = UserCreationForm.Meta.fields + ('email', 'role',) 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Task

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=User.ROLE_CHOICES)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }