from django.contrib.auth.views import (
    PasswordResetDoneView, 
    PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy
from . import views
from .views import ResetPasswordConfirmView

app_name = 'quotes'

urlpatterns = [
    path('', views.quote_list, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('author/<str:name>/', views.author_detail, name='author_detail'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),

    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path(
        'reset-password/done/',
        PasswordResetDoneView.as_view(template_name='quotes/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset-password/confirm/<uidb64>/<token>/',
        ResetPasswordConfirmView.as_view(
            template_name='quotes/password_reset_confirm.html',
            success_url=reverse_lazy('quotes:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset-password/complete/',
        PasswordResetCompleteView.as_view(template_name='quotes/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]