from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.

# pk_e632a59aa5134923b1e06e4c18cdc481


def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']

        base_url = "https://cloud.iexapis.com/stable/stock/"
        auth_token = "pk_e632a59aa5134923b1e06e4c18cdc481"
        params = "/batch?types=quote,news,chart&range=1m&last=10&token="
        api_request = requests.get(base_url + ticker + params + auth_token)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"

        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol"})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('add_stock')
    else:

        tickers = Stock.objects.all()
        output = []

        base_url = "https://cloud.iexapis.com/stable/stock/market/batch?symbols="
        auth_token = "pk_e632a59aa5134923b1e06e4c18cdc481"
        params = "&types=quote,news,chart&range=1m&last=10&token="

        symbols = ""
        for ticker in tickers:
            symbols += str(ticker)+','
        symbols = symbols[:-1]

        api_request = requests.get(base_url + symbols + params + auth_token)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"

        output = []

        for item in api:
            output.append(api[item]["quote"])

        # for ticker_item in tickers:
        #     api_request = requests.get(
        #         base_url + str(ticker_item) + params + auth_token)
        #     try:
        #         api = json.loads(api_request.content)
        #         output.append(api['quote'])
        #     except Exception as e:
        #         api = "Error"
        return render(request, 'add_stock.html', {'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted!")
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
