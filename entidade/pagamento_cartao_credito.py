from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from entidade.paciente import Paciente
from entidade.pagamento import Pagamento

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class PagamentoCartaoCredito(Pagamento):
    def __init__(self, id: int, data: date, atendimento: Atendimento,
                 paciente: Paciente, valor_pago: Decimal,
                 numero_cartao: str, bandeira: str):
        super().__init__(id, data, atendimento, paciente, valor_pago)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str):
        self.__numero_cartao = numero_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira

    def descrever_forma(self) -> str:
        return f"Cartão de crédito {self.__bandeira} final {self.__numero_cartao[-4:]}"
