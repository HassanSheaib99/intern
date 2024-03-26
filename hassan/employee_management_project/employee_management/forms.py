from django import forms
from .models import CustomUser
from django.contrib.auth.models import User
from .models import Employee

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'department']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    department = forms.CharField(max_length=100)  
class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['title', 'department', 'email', 'phone_number', 'vacation_days', 'position']

    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user.user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user