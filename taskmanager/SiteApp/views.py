from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

def index(request):
    page_obj=item = Product.objects.all()

    item_name = request.GET.get("search")
    if item_name != '' and item_name is not None:
        page_obj = item.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "items":item, "page_obj":page_obj
    }
    return render(request, "SiteApp/index.html", context)

class ProductListView(ListView):
    model = Product
    template_name = "SiteApp/index.html"
    context_object_name = "items"
    paginate_by = 3

#def indexItem(request, item_id):
 #   items = Product.objects.get(id=item_id)
  #  context = {
  #      "item":items
  #  }
  #  return render(request, "SiteApp/detail.html", context=context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "SiteApp/detail.html"
    context_object_name = "item"

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

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("SiteApp:index")

def mainpage(request):
    return HttpResponse("Главная страница")

