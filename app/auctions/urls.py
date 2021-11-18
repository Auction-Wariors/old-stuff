"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views


app_name = 'auctions'


urlpatterns = [
    # "auctions/"
    path('create/', views.add_auction, name='add_auction'),
    path('edit/<int:auction_id>/', views.update_auction, name='update_auction'),
    path('payment/<int:auction_id>/', views.payment_auction, name='payment_auction'),
    path('payment/success/<int:auction_id>/', views.payment_ok, name='payment_ok'),
    path('<int:pk>/', views.auction_detail, name='auction_detail'),

]


