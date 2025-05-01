"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.views import (
    LoginView,
    RefreshView,
    ValidateTokenView,
    LogoutView,
    UserListCreateView,
    UserDetailView,
)
from django.views.generic import TemplateView, RedirectView
from predictions.views import PredictionView, PredictionListView, PredictionDeleteView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation with Swagger and JWT Authentication",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    # Admin Interface
    path("admin/", admin.site.urls),

    # Documentação Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Autenticação JWT
    path('api/login/', LoginView.as_view(), name='token_obtain_pair'),                  # Login
    path('api/refresh/', RefreshView.as_view(), name='token_refresh'),                  # Refresh token
    path('api/validate-token/', ValidateTokenView.as_view(), name='validate_token'),    # Validate token
    path('api/logout/', LogoutView.as_view(), name='logout'),                           # Logout

    # Gerenciamento de Usuários
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),  # Listar/Criar usuários
    path('api/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),  # Detalhes/Atualizar/Excluir usuário

    # Predição
    path('api/predict/', PredictionView.as_view(), name='predict'),                                 # Criar uma predição
    path('api/predictions/', PredictionListView.as_view(), name='prediction-list'),                 # Listar predições
    path('api/predictions/<int:pk>/', PredictionDeleteView.as_view(), name='prediction-delete'),    # Deletar predições

    # Frontend
    path('', RedirectView.as_view(url='/login'), name='root_redirect'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),                       # Página de Login
    path('logout/', TemplateView.as_view(template_name='logout.html'), name='logout'),                    # Página de Logout
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),           # Dashboard
    path('users/', TemplateView.as_view(template_name='users.html'), name='users'),                       # Gerenciamento de Usuários
    path('predictions/', TemplateView.as_view(template_name='predictions.html'), name='predictions'),     # Gerenciamento de Predições
]
