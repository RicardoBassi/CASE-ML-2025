from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Classe de administração simplificada para o modelo CustomUser.

    Esta classe define como o modelo CustomUser será exibido e gerenciado no Django Admin.
    Foca em uma interface limpa e funcional, exibindo apenas os campos mais relevantes.

    Attributes:
        list_display (tuple): Campos exibidos na lista de usuários.
        search_fields (tuple): Campos usados para pesquisa no admin.
        list_filter (tuple): Filtros disponíveis na barra lateral.
    """

    # Campos exibidos na lista de usuários
    list_display = ('email', 'nome_completo', 'telefone', 'is_staff', 'is_superuser')

    # Campos usados para pesquisa
    search_fields = ('email', 'nome_completo', 'telefone')

    # Filtros disponíveis na barra lateral
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Sobrescreve a ordenação padrão para usar 'email' em vez de 'username'
    ordering = ('email',)
