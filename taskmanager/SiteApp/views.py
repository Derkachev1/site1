from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def index(request):
    item = Product.objects.all()
    context = {
        "items":item
    }
    return render(request, "SiteApp/index.html", context)

def indexItem(request, item_id):
    items = Product.objects.get(id=item_id)
    context = {
        "item":items
    }
    return render(request, "SiteApp/detail.html", context=context)

def mainpage(request):
    return HttpResponse("Главная страница")
