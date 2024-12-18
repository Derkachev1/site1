import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render 
from django.urls import reverse, reverse_lazy 
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView

from .models import Product, OrderDetail

def index(request):
    page_obj=item = Product.objects.all()

    item_name = request.GET.get("search")
    if item_name != '' and item_name is not None:
        page_obj = item.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 2)
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
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context

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

@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session=stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types = ["card"],
        line_items = [
            {
                "price_data":{
                    "currency":"usd",
                    "product_data":{
                        "name":product.name,
                    },
                    "unit_amount":int(product.price*100)
                },
                "quantity":1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("SiteApp:success"))+"?session_id+{CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("SiteApp:failed")),
    )
    order = OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({"sessionId":checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "SiteApp/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail, stripe_payment_intent = session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name = "SiteApp/payment_failed.html"

#def mainpage(request):
 #   return HttpResponse("Главная страница")

