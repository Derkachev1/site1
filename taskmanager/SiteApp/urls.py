from django.urls import path
from SiteApp import views

app_name = "SiteApp"

urlpatterns = [
    path('', views.index, name="index"),
    #path('', views.ProductListView.as_view(), name="index"),
    #path('<int:item_id>/', views.indexItem, name="detail"),
    path('<int:pk>/', views.ProductDetailView.as_view(), name="detail"),
    path('additem/', views.add_item, name="add_item"),
    path('updateitem/<int:item_id>/', views.update_item, name="update_item"),
    path('deleteitem/<int:pk>/', views.ProductDeleteView.as_view(), name="delete_item"),
    path('success/', views.PaymentSuccessView.as_view(), name="success"),
    path('failed/', views.PaymentFailedView.as_view(), name="failed"),
    path('api/checkout-session/<int:id>/', views.update_item, name="api_checkout_session"),
    #path('mainpage/', views.mainpage),
]