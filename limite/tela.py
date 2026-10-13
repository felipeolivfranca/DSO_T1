from abc import ABC, abstractmethod
from datetime import date, time
from decimal import Decimal


class Tela(ABC):
    def le_num_inteiro(self, mensagem: str, validos: list = None) -> int:
        pass

    def le_texto(self, mensagem: str) -> str:
        pass

    def le_valor_decimal(self, mensagem: str) -> Decimal:
        pass

    def le_data(self, mensagem: str) -> date:
        pass

    def le_hora(self, mensagem: str) -> time:
        pass

    def mostra_mensagem(self, mensagem: str):
        pass

    @abstractmethod
    def mostra_menu(self) -> int:
        pass
