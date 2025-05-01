from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Prediction
from .serializers import PredictionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ml_models.predictor import Regressor


class PredictionView(APIView):
    """
    Endpoint para realizar predições usando o modelo de regressão.

    Requer autenticação JWT.
    O usuário envia os valores das features de entrada e recebe as predições geradas pelo modelo.
    As predições e os dados de entrada são armazenados no banco de dados.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Realizar uma predição usando o modelo de regressão.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['X1', 'X2', 'X3', 'X6', 'X7', 'X8'],
            properties={
                'X1': openapi.Schema(type=openapi.TYPE_NUMBER, description="Feature X1"),
                'X2': openapi.Schema(type=openapi.TYPE_NUMBER, description="Feature X2"),
                'X3': openapi.Schema(type=openapi.TYPE_NUMBER, description="Feature X3"),
                'X6': openapi.Schema(type=openapi.TYPE_INTEGER, description="Feature X6"),
                'X7': openapi.Schema(type=openapi.TYPE_NUMBER, description="Feature X7"),
                'X8': openapi.Schema(type=openapi.TYPE_INTEGER, description="Feature X8"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Predição realizada com sucesso.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "prediction": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "heating_load": openapi.Schema(type=openapi.TYPE_NUMBER),
                                "cooling_load": openapi.Schema(type=openapi.TYPE_NUMBER),
                            },
                        ),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(description="Requisição inválida - Dados ausentes ou incorretos."),
            500: openapi.Response(description="Erro interno no servidor."),
        }
    )
    def post(self, request):
        try:
            # Dados enviados pelo usuário
            data = request.data

            # Validar os campos obrigatórios
            required_fields = ['X1', 'X2', 'X3', 'X6', 'X7', 'X8']
            if not all(field in data for field in required_fields):
                return Response(
                    {"error": "Todos os campos são obrigatórios: X1, X2, X3, X6, X7, X8"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convertendo valores corretamente
            input_data = {
                'X1': float(data['X1']),
                'X2': float(data['X2']),
                'X3': float(data['X3']),
                'X6': int(data['X6']),
                'X7': float(data['X7']),
                'X8': int(data['X8']),
            }

            # Realizar a predição usando o módulo separado
            regressor = Regressor()
            prediction_output = regressor.predict(input_data)

            # Salvar no banco de dados
            prediction_record = Prediction.objects.create(
                user=request.user,
                input_data=input_data,
                output_data=prediction_output
            )

            return Response({
                "prediction": prediction_record.output_data,
                "message": "Predição registrada com sucesso."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictionListView(APIView):
    """
    Endpoint para listar todas as predições realizadas pelo usuário logado.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Listar todas as predições realizadas pelo usuário logado.",
        responses={
            200: PredictionSerializer(many=True),  # Indica que o serializer será usado para a resposta
            401: openapi.Response(description="Não autenticado."),
        }
    )
    def get(self, request, *args, **kwargs):
        predictions = Prediction.objects.filter(user=request.user)
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PredictionDeleteView(APIView):
    """
    Endpoint para excluir uma predição específica.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        """
        Lida com requisições DELETE para excluir uma predição específica.

        Args:
            request (HttpRequest): O objeto de requisição.
            pk (int): ID da predição a ser excluída.

        Returns:
            Response: Resposta JSON confirmando a exclusão ou mensagem de erro.
        """
        try:
            prediction = Prediction.objects.get(id=pk, user=request.user)
            prediction.delete()
            return Response(
                {"message": "Predição excluída com sucesso."},
                status=status.HTTP_200_OK
            )
        except Prediction.DoesNotExist:
            return Response(
                {"error": "Predição não encontrada ou você não tem permissão para excluí-la."},
                status=status.HTTP_404_NOT_FOUND
            )
