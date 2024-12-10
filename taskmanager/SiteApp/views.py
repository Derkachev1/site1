from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required

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

@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES["upload"]
        seller = request.user
        item = Product(name=name, price=price, description=description, image=image, seller=seller)
        item.save()
    return render(request, "SiteApp/additem.html")

def update_item(request, item_id):
    item = Product.objects.get(id=item_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get("upload", item.image)
        item.save()
        return redirect("/SiteApp/")
    context = {
        "item":item
    }
    return render(request, "SiteApp/updateitem.html", context)

def delete_item(request, item_id):
    item = Product.objects.get(id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("/SiteApp/")
    context = {
        "item":item
    }
    return render(request, "SiteApp/deleteitem.html", context)

def mainpage(request):
    return HttpResponse("Главная страница")

