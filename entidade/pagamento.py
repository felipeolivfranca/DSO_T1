from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from entidade.paciente import Paciente

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class Pagamento(ABC):
    @abstractmethod
    def __init__(self, id: int, data: date, atendimento: Atendimento,
                 paciente: Paciente, valor_pago: Decimal):
        self.__id = id
        self.__data = data
        self.__atendimento = atendimento
        self.__paciente = paciente
        self.__valor_pago = valor_pago

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def atendimento(self) -> Atendimento:
        return self.__atendimento

    @atendimento.setter
    def atendimento(self, atendimento: Atendimento):
        self.__atendimento = atendimento

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @property
    def valor_pago(self) -> Decimal:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: Decimal):
        self.__valor_pago = valor_pago

    @abstractmethod
    def descrever_forma(self) -> str:
        pass

    def calcular_valor_restante(self) -> Decimal:
        return self.__atendimento.calcularTotalRestante()
