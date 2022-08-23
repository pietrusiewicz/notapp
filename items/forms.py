from django import forms

class LoginForm(forms.Form):
    usname = forms.CharField(label="username")
    passwd = forms.CharField(label="password", widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    passwd1 = forms.CharField(label="new password", widget=forms.PasswordInput)
    passwd2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

class CreateUserForm(forms.Form):
    usname = forms.CharField(label="username")
    email = forms.CharField(label="email")
    passwd1 = forms.CharField(label="password", widget=forms.PasswordInput)
    passwd2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

class AddItemForm(forms.Form):
    itemname = forms.CharField(label="item name")
    price = forms.FloatField(label="price")
    count = forms.IntegerField(label="count")
