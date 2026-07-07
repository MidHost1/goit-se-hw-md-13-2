from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quote_list, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('author/<str:name>/', views.author_detail, name='author_detail'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]