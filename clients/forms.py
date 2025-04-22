from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Client

User = get_user_model()


class ClientModelForm(forms.ModelForm):
    class Meta: 
        model = Client
        fields = [
            'name',
            'address',
            'area',
            'city',
            'email',
            'phone_number',
            'source',
            'role',
            'contacted',
            'follow_up_date',
            'birthday',
            'detail',
            'agent',
        ]
        widgets = {
            'detail': forms.Textarea(attrs={'rows': 4}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") 

class UploadClientsForm(forms.Form):
    excel_file = forms.FileField(
        label="Select Excel File",
        help_text="Please upload an Excel file (.xlsx or .xls)",
    )