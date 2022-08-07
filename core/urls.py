
from django.urls import path, include
from .views import home_view, crypto_view, stocks_view, base_view, sports_view

app_name = "core"

urlpatterns = [
    path("", base_view, name="base"),
    path("home", home_view, name="home"),
    path("crypto", crypto_view, name="crypto"),
    path("stocks", stocks_view, name="stocks"),
    path("sports", sports_view, name="sports"),
    
]
