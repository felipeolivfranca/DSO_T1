from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from entidade.paciente import Paciente
from entidade.pagamento import Pagamento

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class PagamentoPix(Pagamento):
    def __init__(self, id: int, data: date, atendimento: Atendimento,
                 paciente: Paciente, valor_pago: Decimal, cpf_pagador: str):
        super().__init__(id, data, atendimento, paciente, valor_pago)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = cpf_pagador

    def descrever_forma(self) -> str:
        pass

    def calcular_valor_restante(self) -> Decimal:
        pass
