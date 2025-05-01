from django.db import models
from accounts.models import CustomUser


class Prediction(models.Model):
    """
    Modelo para armazenar as predições realizadas pelos usuários.

    Fields:
        user (ForeignKey): Usuário que realizou a predição.
        input_data (JSONField): Dados de entrada fornecidos pelo usuário.
        output_data (JSONField): Resultados gerados pelo modelo.
        created_at (DateTimeField): Data e hora da predição.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='predictions')
    input_data = models.JSONField(help_text="Dados de entrada fornecidos pelo usuário.")
    output_data = models.JSONField(help_text="Resultados gerados pelo modelo.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predição de {self.user.email} em {self.created_at}"
