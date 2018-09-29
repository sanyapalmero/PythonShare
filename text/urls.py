from django.urls import include, path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddView.as_view(), name='add'),
    path('upd/<int:text_id>', views.UpdView.as_view(), name='upd'),
    path('del/<int:text_id>', views.DelView.as_view(), name='del'),
    path('text/<int:text_id>', views.DetailView.as_view(), name='detail'),
    path('edit/<int:text_id>', views.EditView.as_view(), name='edit'),
    path('delete/<int:text_id>', views.DeleteView.as_view(), name='delete'),
    path('create/', views.CreateView.as_view(), name='create')
]
