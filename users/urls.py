from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Web views
    path('', views.UserListView.as_view(), name='user-list'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # API endpoints
    path('api/login/', views.LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='api-profile'),
    path('api/branches/', views.BranchListAPIView.as_view(), name='api-branches'),
] 