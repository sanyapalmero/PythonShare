from django.urls import include, path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout')
]