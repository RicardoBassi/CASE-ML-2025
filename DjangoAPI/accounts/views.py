# from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# from rest_framework.views import APIView

# accounts/views.py
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
from .models import CustomUser


class LoginView(TokenObtainPairView):
    """
    Endpoint de Autenticação JWT

    Permite que os usuários se autentiquem e recebam tokens de acesso/refresh.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Autenticar usuário e retornar tokens JWT",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description="Autenticação bem-sucedida"),
            401: openapi.Response(description="Credenciais inválidas"),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Lida com requisições POST para autenticar um usuário.

        Args:
            request (HttpRequest): O objeto de requisição contendo email e senha.

        Returns:
            Response: Resposta JSON com tokens de acesso e refresh em caso de sucesso, ou mensagem de erro em caso de falha.
        """
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class RefreshView(TokenRefreshView):
    """
    Endpoint de Atualização de Token

    Gera um novo token de acesso usando um token de refresh válido.
    """
    @swagger_auto_schema(
        operation_description="Gerar novo token de acesso usando token de refresh",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description="Novo token de acesso gerado"),
            401: openapi.Response(description="Token de refresh inválido ou expirado")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Lida com requisições POST para atualizar um token de acesso.

        Args:
            request (HttpRequest): O objeto de requisição contendo o token de refresh.

        Returns:
            Response: Resposta JSON com um novo token de acesso em caso de sucesso, ou mensagem de erro em caso de falha.
        """
        return super().post(request, *args, **kwargs)
    

# accounts/views.py
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class ValidateTokenView(TokenVerifyView):
    """
    Endpoint de Validação de Token
    Verifica a validade do token JWT e retorna informações do usuário autenticado.
    """
    
    @swagger_auto_schema(
        operation_description="Validar token JWT e recuperar dados do usuário",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token'],
            properties={
                'token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Token JWT para validação'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Token válido",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "user": UserSerializer().data,
                    }
                )
            ),
            401: openapi.Response(
                description="Token inválido/expirado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            500: openapi.Response(description="Erro interno no servidor")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            # Verifica o token usando a lógica do SimpleJWT
            response = super().post(request, *args, **kwargs)
            
            if response.status_code != 200:
                return response  # Retorna erro 401 se token inválido
            
            # Obtém o token do corpo da requisição
            token = request.data.get('token')
            if not token:
                return Response({
                    "valid": False,
                    "message": "Token não fornecido"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            try:
                # Decodifica o token para obter o payload
                untyped_token = UntypedToken(token)
                user_id = untyped_token.get('user_id')
                
                # Busca o usuário no banco de dados
                User = get_user_model()
                user = User.objects.get(id=user_id)
                
                # Serializa os dados do usuário
                serializer = UserSerializer(user)
                
                return Response({
                    "valid": True,
                    "user": serializer.data
                }, status=status.HTTP_200_OK)
                
            except (InvalidToken, TokenError) as e:
                return Response({
                    "valid": False,
                    "message": f"Token inválido: {str(e)}"
                }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    "valid": False,
                    "message": "Usuário não encontrado"
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({
                "valid": False,
                "message": f"Erro interno: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(TokenBlacklistView):
    """
    Endpoint de Logout

    Invalida o token de refresh adicionando-o à lista negra.
    """
    @swagger_auto_schema(
        operation_description="Invalidar token de refresh e deslogar o usuário (adicionar token à lista negra)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Token de refresh para adicionar à lista negra'
                ),
            },
        ),
        responses={
            200: openapi.Response(description="Logout realizado com sucesso"),
            401: openapi.Response(description="Token inválido")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Lida com requisições POST para invalidar um token de refresh e deslogar o usuário.

        Args:
            request (HttpRequest): O objeto de requisição contendo o token de refresh.

        Returns:
            Response: Resposta JSON confirmando o logout bem-sucedido.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
        return response


class UserListCreateView(generics.ListCreateAPIView):
    """
    Endpoint de Gerenciamento de Usuários

    Permite que administradores listem usuários e criem novas contas.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Listar todos os usuários (somente administradores)",
        responses={
            200: openapi.Response(description="Lista de usuários"),
            401: openapi.Response(description="Não autenticado"),
            403: openapi.Response(description="Proibido - Acesso de administrador necessário"),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Lida com requisições GET para listar todos os usuários.

        Args:
            request (HttpRequest): O objeto de requisição.

        Returns:
            Response: Resposta JSON contendo uma lista de todos os usuários.
        """
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Criar novo usuário (somente administradores)",
        request_body=UserSerializer,
        responses={
            201: openapi.Response(description="Usuário criado com sucesso", schema=UserSerializer),
            400: openapi.Response(description="Requisição inválida - Dados inválidos"),
            403: openapi.Response(description="Proibido - Acesso de administrador necessário")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Lida com requisições POST para criar um novo usuário.

        Args:
            request (HttpRequest): O objeto de requisição contendo os dados do usuário.

        Returns:
            Response: Resposta JSON com os detalhes do usuário criado em caso de sucesso, ou mensagem de erro em caso de falha.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint de Detalhes de Usuário

    Permite que administradores recuperem/atualizem/excluam usuários específicos.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Recuperar detalhes do usuário (somente administradores)",
        responses={
            200: openapi.Response(description="Detalhes do usuário recuperados com sucesso", schema=UserSerializer),
            403: openapi.Response(description="Proibido - Acesso de administrador necessário"),
            404: openapi.Response(description="Usuário não encontrado")
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Lida com requisições GET para recuperar detalhes de um usuário específico.

        Args:
            request (HttpRequest): O objeto de requisição.
            kwargs (dict): Parâmetros da URL, incluindo o ID do usuário.

        Returns:
            Response: Resposta JSON contendo os detalhes do usuário.
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualizar detalhes do usuário (somente administradores)",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(description="Usuário atualizado com sucesso"),
            400: openapi.Response(description="Requisição inválida - Dados inválidos"),
            403: openapi.Response(description="Proibido - Acesso de administrador necessário"),
            404: openapi.Response(description="Usuário não encontrado")
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Lida com requisições PUT para atualizar detalhes de um usuário específico.

        Args:
            request (HttpRequest): O objeto de requisição contendo os dados atualizados do usuário.
            kwargs (dict): Parâmetros da URL, incluindo o ID do usuário.

        Returns:
            Response: Resposta JSON com os detalhes atualizados do usuário em caso de sucesso, ou mensagem de erro em caso de falha.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Usuário atualizado com sucesso", "user": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Excluir usuário (somente administradores)",
        responses={
            200: openapi.Response(description="Usuário excluído com sucesso"),
            204: openapi.Response(description="Usuário excluído com sucesso"),
            403: openapi.Response(description="Proibido - Acesso de administrador necessário"),
            404: openapi.Response(description="Usuário não encontrado")
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Lida com requisições DELETE para remover um usuário específico.

        Args:
            request (HttpRequest): O objeto de requisição.
            kwargs (dict): Parâmetros da URL, incluindo o ID do usuário.

        Returns:
            Response: Resposta JSON confirmando a exclusão bem-sucedida.
        """
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Usuário excluído com sucesso"}, status=status.HTTP_200_OK)
