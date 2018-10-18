from django.urls import include, path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.ProfileSettingsView.as_view(), name='settings'),
    path(
        'settings/setavatar',
        views.UpdateAvatarView.as_view(),
        name='setavatar'),
    path(
        'settings/setpass', views.UpdatePasswordView.as_view(), name='setpass')
]
