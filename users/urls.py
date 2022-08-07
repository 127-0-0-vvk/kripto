
from django.urls import path
from .views import ( logout_view, 
login_view, 
signup_view, 
passwordreset_view, 
forgot_password_request_view, 
forgot_password_response_view,
)
app_name="users"

urlpatterns = [
       path("logout/", logout_view, name="logout"),
       path("login/", login_view, name="login"),
       path("signup/", signup_view, name="signup"),
       path("passwordreset/", passwordreset_view, name="password-reset"),
       path("forgotpassword/", forgot_password_request_view, name="forgot-password"),
       path("forgotpassword/<token>/", forgot_password_response_view, name="forgot-password-response"),
]
