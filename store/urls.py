from django.contrib import admin
from django.urls import path
from .views import index, signup,login,logout,cart

urlpatterns = [
    path('', index.as_view(),name='homepage'),
    path('signup/', signup, name='signup'), 
    path('login/', login, name='login'),  # URL pattern for signup view
    path('logout/', logout, name='logout'),
    path('cart/', cart.as_view(), name='cart'),
    
]

