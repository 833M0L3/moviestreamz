from django import forms
from django.contrib.auth.models import User

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation
