from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import UserLoginForm, UserSignupForm, UserPasswordResetForm, UserForgotPasswordForm, UserForgotPasswordResetForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ForgotPasswordToken
from datetime import datetime, timedelta
from django.utils import timezone
from random import choice
from django.db.models.query import QuerySet

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logged OUT!!!")
    return redirect("core:base")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/home")
    
    
    form = UserLoginForm(data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user =  authenticate(
                request, username=username, password=password
                )
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Logged IN!!!!")
                return redirect(request.GET.get('next') or "/home")
        
        messages.add_message(
            request, messages.WARNING, "Invalid username or password !"
            )
        context = {'form':form}
        return render(request, "users/login.html", context)
            
            
    if request.method == "GET":
        context = {'form':form}
        return render(request, "users/login.html", context)
    
    
def signup_view(request):
        if request.user.is_authenticated:
         return redirect("/")
    
    
        form = UserSignupForm(data=request.POST or None)
    
        if request.method == "POST":
         if form.is_valid():
             username = form.cleaned_data.get('username')
             email = form.cleaned_data.get('email')
             password = form.cleaned_data.get('password')
            
             if User.objects.filter(
                 Q(username=username) | Q(email=email)
             ).exists():
                   messages.add_message(
                       request, 
                       messages.INFO, 
                       "Username or email already exists! Try Loging in.",
                   )
                   context = {'form':form}
                   return render(request, "users/signup.html", context)
              
             new_user = User(
                username=username, email=email)
             new_user.set_password(password)
             new_user.save()
             
             messages.add_message(request, messages.SUCCESS, " Signedup, Continue to login ")
             return redirect("users:login")
                
                
        
        messages.add_message(
            request, messages.WARNING, "Invalid username or password !"
            )
        context = {'form':form}
        return render(request, "users/signup.html", context)
            
            
        if request.method == "GET":
           context = {'form':form}
           return render(request, "users/signup.html", context)
      
    
    
def passwordreset_view(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    
    form = UserPasswordResetForm(data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            
            user =  authenticate(
                request, username=request.user.username, password= current_password
                )
            if user is not None:
                request.user.set_password(new_password)
                request.user.save()
                messages.add_message(request, messages.SUCCESS, "Password Updated")
                return redirect( "/")
            else:
                messages.add_message(request, messages.WARNING, " Incorrect password, please try again!")
                context = {'form':form}
                return render(request, "users/password-reset.html", context)
                
        
        messages.add_message(
            request, messages.WARNING, "Invalid password !"
            )
        context = {'form':form}
        return render(request, "users/password-reset.html", context)
            
            
    if request.method == "GET":
        context = {'form':form}
        return render(request, "users/password-reset.html", context)


def forgot_password_request_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    
    form = UserForgotPasswordForm(data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            
            queryset = User.objects.filter(Q(username=username_or_email)|Q(email=username_or_email))
            
            if not queryset.exists():
                messages.add_message(request, messages.INFO, "User not found!")
                context = {"form": form}
                return render(request, "users/forgot-password-request.html", context)
            
            user = queryset.first()
            
            queryset = ForgotPasswordToken.objects.filter(user=user)
            
            if queryset.exists():
                password_reset_token = queryset.first()
                
                if password_reset_token.updated < timezone.now() - timedelta(minutes=15):
                 messages.add_message(request, message.WARNING, " Password was updated recently , wait for 15 minutes!" )
                 context = {'form':form}
                 return render(
                     request,
                     "user/forgot-password-request.html",
                     context,
                 )
                else:
                  password_reset_token.delete()
            #RESEET THE PASSWORD
        token = "".join(
            [
                choice(
                    'qwertyuiopasdfghjklzxcvbnm123456789QWERTYUIOPASDFGHJKLZXCVBNM'
                    ) for _ in range(15)
                ]
            ) 
        password_reset_token= ForgotPasswordToken(
            user=user, token=token
            )
        password_reset_token.save()
           
           #sendmail()
        print(
            f"Goto: http://127.0.0.1:8000/users/forgotpassword/{token}"
            )
           
        messages.add_message(
            request, messages.SUCCESS, "We have sent an email, to rest the password"
        )
        context = {'form':form}
        return render(
                     request,
                     "users/forgot-password-request.html",
                     context,
        )
           
        
        
        messages.add_message(
            request, messages.WARNING, "Invalid Username !"
            )
        context = {'form':form}
        return render(
                     request,
                     "user/forgot-password-request.html",
                     context,
         )
            
            
    if request.method == "GET":
        context = {'form':form}
        return render(request, "users/forgot-password-request.html", context)


def forgot_password_response_view(request, token):
    if request.user.is_authenticated:
        return redirect("/")
    
    queryset = ForgotPasswordToken.objects.filter(token=token)
    
    if not queryset.exists():
        return redirect("/")
    
    forgot_password_token = queryset.first()
    user = forgot_password_token.user
    
    form = UserForgotPasswordResetForm(data=request.POST)
    
    if request.method == "GET":
        context ={"form":form}
        return render(request, "users/forgot-password-response.html", context)
    
    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data.get("password")
            
            user.set_password(password)
            user.save()
            token = "".join(
            [
                choice(
                    'qwertyuiopasdfghjklzxcvbnm123456789QWERTYUIOPASDFGHJKLZXCVBNM'
                    ) for _ in range(15)
                ]
            ) 
            forgot_password_token.token = token
            forgot_password_token.save()
            messages.add_message(request, messages.SUCCESS, "Password updated..")
            
            return redirect("users:login")