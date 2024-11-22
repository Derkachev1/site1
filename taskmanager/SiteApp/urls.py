from django.urls import path
from SiteApp import views

app_name = "SiteApp"

urlpatterns = [
    path('', views.index),

    path('<int:item_id>/', views.indexItem, name="detail"),

    path('mainpage/', views.mainpage)
]