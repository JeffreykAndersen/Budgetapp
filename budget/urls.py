from django.urls import path
from . import views

urlpatterns = [
    # USER LOGGING, CREATION, AND LOGOUT
    path('', views.log_page),
    path('register_user', views.register_user),
    path('log_in', views.log_in),
    path('log_out', views.logout),
    # HOME PAGE
    path('home', views.home),
    # EXPENSE AND INCOME
    path('add_expense', views.add_expense),
    path('add_income', views.add_income),
]
