from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta: 
        model = Lead
        fields = [
            'name',
            'address',
            'area',
            'city',
            'email',
            'phone_number',
            'source',
            'status',
            'contacted',
            'follow_up_date',
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

class UploadLeadsForm(forms.Form):
    excel_file = forms.FileField(
        label="Select Excel File",
        help_text="Please upload an Excel file (.xlsx or .xls)",
    )

class LeadDataForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)
    area = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    status = forms.CharField(max_length=255)  # Validate against Lead.STATUS choices
    follow_up_date = forms.DateField(required=False)
    agent_username = forms.CharField(max_length=150, required=False)

    def clean_status(self):
        status = self.cleaned_data["status"]
        valid_statuses = [choice[0] for choice in Lead.STATUS]
        if status not in valid_statuses:
            raise forms.ValidationError("Invalid status.")
        return status

    def clean_agent_username(self):
        agent_username = self.cleaned_data["agent_username"]
        if agent_username:
            try:
                Agent.objects.get(user__username=agent_username)
            except Agent.DoesNotExist:
                raise forms.ValidationError("Agent does not exist.")
        return agent_username