from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('search/', views.search, name='search'),
    path('', views.check_login, name='check_login'),
    path('create-user/', views.create_user, name='create-user'),
    path('logout/', views.logout_view, name='logout'),

]
