import joblib
import pandas as pd
from django.conf import settings
from typing import Dict, Tuple


class Regressor:
    """
    Classe responsável por carregar o modelo e o scaler, e executar predições.
    """

    def __init__(self):
        self.model, self.scaler = self._load_model_and_scaler()

    def _load_model_and_scaler(self) -> Tuple[object, object]:
        """
        Carrega o modelo e o scaler salvos previamente.

        Returns:
            Tuple: Instância do modelo e do scaler.
        """
        model_path = settings.BASE_DIR / 'ml_models' / 'xgboost_regressor_model.pkl'
        scaler_path = settings.BASE_DIR / 'ml_models' / 'xgboost_scaler.pkl'

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        return model, scaler

    def predict(self, input_data: Dict[str, float]) -> Dict[str, float]:
        """
        Realiza a predição com base nos dados de entrada fornecidos.

        Args:
            input_data (dict): Dicionário contendo os valores das features de entrada.

        Returns:
            dict: Resultados da predição com carga de aquecimento e resfriamento.
        """
        features = ['X1', 'X2', 'X3', 'X6', 'X7', 'X8']

        # Validar se todos os campos necessários estão presentes
        for feature in features:
            if feature not in input_data:
                raise ValueError(f"Campo obrigatório ausente: {feature}")

        # Criar DataFrame com os dados
        df = pd.DataFrame([[input_data[feature] for feature in features]], columns=features)

        # Aplicar scaler
        scaled = self.scaler.transform(df)

        # Realizar predição
        prediction = self.model.predict(scaled)

        return {
            "heating_load": round(float(prediction[0][0]), 2),
            "cooling_load": round(float(prediction[0][1]), 2),
        }
