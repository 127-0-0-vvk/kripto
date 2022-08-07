from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=32, 
        min_length=1, 
        widget=forms.TextInput(attrs={'class': 'forms-control-sm'}),
        )
    password = forms.CharField(
        max_length=32, 
        min_length=1, 
        widget=forms.PasswordInput(attrs={'class': 'forms-control-sm'}),
        )
    
    
    
    
class UserSignupForm(forms.Form):
    username = forms.CharField(
        max_length=32, 
        min_length=1, 
        widget=forms.TextInput(attrs={'class': 'forms-control-sm'}),
        )
    email = forms.CharField(
         max_length=32, 
        min_length=8, 
        widget=forms.EmailInput(attrs={'class': 'forms-control-sm'}),
        )
    password = forms.CharField(
        max_length=32, 
        min_length=5, 
        widget=forms.PasswordInput(attrs={'class': 'forms-control-sm'}),
        )
    
class UserPasswordResetForm(forms.Form):
        current_password= forms.CharField(
            max_length=32, 
            min_length=5, 
            widget=forms.PasswordInput(attrs={'class': 'forms-control-sm'}),
        )

        new_password = forms.CharField(
             max_length=32, 
             min_length=5, 
             widget=forms.PasswordInput(attrs={'class': 'forms-control-sm'}),
        )
        
        
        
class UserForgotPasswordForm(forms.Form):
    username_or_email= forms.CharField(
        max_length=32, 
        min_length=1, 
        widget=forms.TextInput(attrs={'class': 'forms-control-sm'}),
        )
    
class UserForgotPasswordResetForm(forms.Form):
    password = forms.CharField(
        max_length=32, 
        min_length=5, 
        widget=forms.PasswordInput(attrs={'class': 'forms-control-sm'}),
        )
    