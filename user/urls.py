from django.urls import include, path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
]
