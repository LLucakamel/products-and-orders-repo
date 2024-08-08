from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('new/', views.order_create, name='order_new'),
    path('edit/<int:id>/', views.order_update, name='order_edit'),
    path('delete/<int:id>/', views.order_delete, name='order_delete'),
]
