from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo CustomUser.

    Este serializer lida com a criação e atualização de instâncias de usuário,
    incluindo a criação segura de senhas hashadas.

    Fields:
        id (int): ID do usuário (somente leitura).
        email (str): Endereço de e-mail do usuário (obrigatório e único).
        nome_completo (str): Nome completo do usuário (obrigatório).
        telefone (str): Número de telefone do usuário (obrigatório).
        password (str): Senha do usuário (escrever apenas).

    Extra kwargs:
        password: {'write_only': True} - A senha não é incluída na resposta serializada.
        id: {'read_only': True} - O ID não pode ser alterado.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nome_completo', 'telefone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Cria uma nova instância de usuário com uma senha hashada.

        Args:
            validated_data (dict): Dados validados contendo email, nome_completo,
                                   telefone e password.

        Returns:
            CustomUser: A instância de usuário recém-criada.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nome_completo=validated_data['nome_completo'],
            telefone=validated_data['telefone'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Atualiza uma instância de usuário existente.

        Lida com a atualização segura de senhas, caso a senha esteja presente nos dados validados.

        Args:
            instance (CustomUser): A instância de usuário a ser atualizada.
            validated_data (dict): Dados validados contendo campos a serem atualizados.

        Returns:
            CustomUser: A instância de usuário atualizada.
        """
        if 'password' in validated_data:
            # Atualiza a senha de forma segura
            instance.set_password(validated_data['password'])
            validated_data.pop('password')  # Remove a senha dos dados validados
        return super().update(instance, validated_data)
