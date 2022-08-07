from django.shortcuts import render
import requests
from django.http import HttpResponse

def base_view(request):
    return render(request, "core/base.html")

def home_view(request):
    return render(request, "core/home.html")

def sports_view(request):
    return render(request, "core/sports.html")



def crypto_view(request):
    url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    data = requests.get(url).json()
    #return HttpResponse(data)
    context = {'data':data}
    return render(request, "core/crypto.html", context)

def stocks_view(request):
    return render(request, "core/stocks.html")