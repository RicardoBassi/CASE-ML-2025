from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Prediction.

    Serializa os dados de entrada, saída e metadados da predição.
    """

    # Campos explícitos com 'source'
    id = serializers.IntegerField(read_only=True, help_text="ID único da predição.")
    user_email = serializers.CharField(source='user.email', read_only=True, help_text="E-mail do usuário que realizou a predição.")

    # Campos de entrada extraídos de input_data
    input_X1 = serializers.FloatField(source='input_data.X1', help_text="Valor da feature X1 fornecido pelo usuário.")
    input_X2 = serializers.FloatField(source='input_data.X2', help_text="Valor da feature X2 fornecido pelo usuário.")
    input_X3 = serializers.FloatField(source='input_data.X3', help_text="Valor da feature X3 fornecido pelo usuário.")
    input_X6 = serializers.IntegerField(source='input_data.X6', help_text="Valor da feature X6 fornecido pelo usuário.")
    input_X7 = serializers.FloatField(source='input_data.X7', help_text="Valor da feature X7 fornecido pelo usuário.")
    input_X8 = serializers.IntegerField(source='input_data.X8', help_text="Valor da feature X8 fornecido pelo usuário.")

    # Campos de saída extraídos de output_data
    output_heating_load = serializers.FloatField(
        source='output_data.heating_load', read_only=True, help_text="Carga de aquecimento estimada pelo modelo."
    )
    output_cooling_load = serializers.FloatField(
        source='output_data.cooling_load', read_only=True, help_text="Carga de resfriamento estimada pelo modelo."
    )

    created_at = serializers.DateTimeField(read_only=True, help_text="Data e hora em que a predição foi registrada.")

    class Meta:
        model = Prediction
        fields = [
            'id',
            'user_email',
            'input_X1',
            'input_X2',
            'input_X3',
            'input_X6',
            'input_X7',
            'input_X8',
            'output_heating_load',
            'output_cooling_load',
            'created_at',
        ]
