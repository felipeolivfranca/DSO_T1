from decimal import Decimal

from entidade.profissional_saude import ProfissionalSaude


class Procedimento:
    def __init__(self, descricao: str, custo: Decimal,
                 profissional_responsavel: ProfissionalSaude, id: int):
        self.__id = id
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional = profissional_responsavel

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def custo(self) -> Decimal:
        return self.__custo

    @custo.setter
    def custo(self, custo: Decimal):
        self.__custo = custo

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = profissional
