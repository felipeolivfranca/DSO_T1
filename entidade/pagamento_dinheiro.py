from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from entidade.paciente import Paciente
from entidade.pagamento import Pagamento

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class PagamentoDinheiro(Pagamento):
    def __init__(self, id: int, data: date, atendimento: Atendimento,
                 paciente: Paciente, valor_pago: Decimal):
        super().__init__(id, data, atendimento, paciente, valor_pago)

    def descrever_forma(self) -> str:
        pass

    def calcular_valor_restante(self) -> Decimal:
        pass
