from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Branch, UserProfile
from .serializers import UserSerializer, BranchSerializer, UserProfileSerializer


class UserListView(LoginRequiredMixin, ListView):
    """Kullanıcı listesi view'ı"""
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CustomUser.objects.select_related('branch').order_by('username')
        
        # Kullanıcı sadece kendi şubesindeki kullanıcıları görebilir (admin hariç)
        if not self.request.user.can_manage_users():
            queryset = queryset.filter(branch=self.request.user.branch)
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        
        return queryset


class ProfileView(LoginRequiredMixin, TemplateView):
    """Kullanıcı profil view'ı"""
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Kullanıcı profilini al veya oluştur
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        context.update({
            'user': user,
            'profile': profile,
        })
        return context


class LoginView(View):
    """Giriş view'ı"""
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            # Şube müdürü ise direkt sipariş oluşturma sayfasına yönlendir
            if hasattr(request.user, 'role') and request.user.role == 'branch_manager':
                return redirect('orders:branch_order_create')
            elif request.user.branch and not request.user.is_staff:
                # Normal şube kullanıcısı da sipariş sayfasına gitsin
                return redirect('orders:branch_order_create')
            else:
                # Admin ve diğer roller dashboard'a gitsin
                return redirect('dashboard')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Hoş geldiniz, {user.get_full_name() or user.username}!')
                    
                    # Kullanıcının rolüne göre yönlendir
                    next_url = request.GET.get('next')
                    if not next_url:
                        # Şube müdürü ise direkt sipariş oluşturma sayfasına yönlendir
                        if hasattr(user, 'role') and user.role == 'branch_manager':
                            next_url = 'orders:branch_order_create'
                        elif user.branch and not user.is_staff:
                            # Normal şube kullanıcısı da sipariş sayfasına gitsin
                            next_url = 'orders:branch_order_create'
                        else:
                            # Admin ve diğer roller dashboard'a gitsin
                            next_url = 'dashboard'
                    return redirect(next_url)
                else:
                    messages.error(request, 'Hesabınız devre dışı bırakılmış.')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
        else:
            messages.error(request, 'Kullanıcı adı ve şifre gerekli.')
        
        return render(request, self.template_name)


class LogoutView(View):
    """Çıkış view'ı"""
    def get(self, request):
        logout(request)
        messages.success(request, 'Başarıyla çıkış yaptınız.')
        return redirect('users:login')


# API Views
class LoginAPIView(generics.GenericAPIView):
    """API Login view'ı"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Giriş başarılı',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Kullanıcı adı veya şifre hatalı'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'status': 'error',
            'message': 'Kullanıcı adı ve şifre gerekli'
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    """API Logout view'ı"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'status': 'success',
                'message': 'Çıkış başarılı'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Çıkış işlemi başarısız'
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """API Profil view'ı"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class BranchListAPIView(generics.ListAPIView):
    """API Şube listesi view'ı"""
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Branch.objects.filter(is_active=True)
        
        # Kullanıcı sadece kendi şubesini görebilir (admin hariç)
        if not self.request.user.can_manage_users():
            queryset = queryset.filter(id=self.request.user.branch_id)
        
        return queryset
