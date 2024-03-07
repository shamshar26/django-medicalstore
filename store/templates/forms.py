from django import forms
from models import Employee
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'password']