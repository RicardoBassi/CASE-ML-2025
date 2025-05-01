from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo CustomUser.

    Este gerenciador usa 'email' como identificador único em vez de 'username'.
    """

    def create_user(self, email, nome_completo, telefone, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email, nome completo, telefone e senha fornecidos.

        Args:
            email (str): Endereço de e-mail do usuário.
            nome_completo (str): Nome completo do usuário.
            telefone (str): Número de telefone do usuário.
            password (str): Senha do usuário (opcional).

        Returns:
            CustomUser: A instância do usuário criada.
        """
        if not email:
            raise ValueError("O campo 'email' é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome_completo=nome_completo,
            telefone=telefone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_completo, telefone, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email, nome completo, telefone e senha fornecidos.

        Args:
            email (str): Endereço de e-mail do superusuário.
            nome_completo (str): Nome completo do superusuário.
            telefone (str): Número de telefone do superusuário.
            password (str): Senha do superusuário (opcional).

        Returns:
            CustomUser: A instância do superusuário criada.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self.create_user(email, nome_completo, telefone, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modelo de usuário personalizado que estende AbstractUser.

    Este modelo substitui o campo 'username' pelo 'email' como identificador único
    e adiciona campos obrigatórios para nome completo e telefone.

    Fields:
        email (EmailField): Endereço de e-mail do usuário (único e obrigatório).
        nome_completo (CharField): Nome completo do usuário (obrigatório).
        telefone (CharField): Número de telefone do usuário (obrigatório).

    Attributes:
        USERNAME_FIELD (str): Define o campo usado para autenticação ('email').
        REQUIRED_FIELDS (list): Lista de campos obrigatórios ao criar um superusuário.
    """

    # Remove o campo 'username' e usa 'email' como identificador único
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="E-mail",
        help_text="Endereço de e-mail do usuário. Deve ser único."
    )
    nome_completo = models.CharField(
        max_length=255,
        verbose_name="Nome Completo",
        help_text="Nome completo do usuário."
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        help_text="Número de telefone do usuário."
    )

    # Configurações do modelo
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'telefone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        """
        Retorna uma representação legível do usuário.

        Returns:
            str: O endereço de e-mail do usuário.
        """
        return self.email
