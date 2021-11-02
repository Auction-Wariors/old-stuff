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


app_name = 'stores'


urlpatterns = [
    # "stores/"
    path('', views.view_all_stores, name='index'),
    path('create/', views.create_store, name='create_store'),
    # TODO remove this when dynamic id on view_store path is in place
    path('1/', views.view_store, name='view_store'),
    # TODO fix dynamic id on view_store path.
    # path('<int:store_id>/', views.view_store, name='view_store'),
    path('<int:store_id>/auctions/create', views.add_auction, name='add_auction'),  # hmm .... rethink this ?
]


