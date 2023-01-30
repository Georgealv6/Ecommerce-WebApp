from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import Customer, Address

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id':'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={ 'class':'form-control mb-3','placeholder': 'Password','id': 'login-pws'}))    

class SignUpForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required') 
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email.'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email')

    #capture data in form 
    #not to have repeated user names
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name    

    #not having miss-matched passwords
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match")
        return cd['password']  

    #make sure users can only use thier email once
    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use, try another")
        return email

    #form styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'Repeat Password'}
            )

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    # user_name = forms.CharField(
    #     label='Username', min_length=4, max_length=50, widget=forms.TextInput(
    #         attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'name', 'id': 'form-name'}))

 
    class Meta:
        model = Customer
        fields = ('email', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=225, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']    
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError('Wrong email address please try another.')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

# address form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Phone"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Address"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Address2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Full Name"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-3 account-form", "placeholder": "Postcode"}
        )