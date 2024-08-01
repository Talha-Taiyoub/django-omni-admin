# forms.py
from django import forms
from segment.models import Branch,Destination

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            'name', 'nick_name', 'destination', 'initial', 'address',
            'status', 'logo', 'overview', 'email', 'telephone',
            'mobile', 'location_iframe'
        ]
    # You can customize error messages and validation here if needed
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email
