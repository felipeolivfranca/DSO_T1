from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from entidade.profissional_saude import ProfissionalSaude

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str,
                 horario_abertura: time, horario_fechamento: time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__profissionais = []
        self.__atendimentos = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        self.__cidade = cidade

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def horario_abertura(self) -> time:
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, abertura: time):
        self.__horario_abertura = abertura

    @property
    def horario_fechamento(self) -> time:
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, fechamento: time):
        self.__horario_fechamento = fechamento

    @property
    def profissionais(self) -> list[ProfissionalSaude]:
        return self.__profissionais

    @property
    def atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    def adicionar_profissional(self, p: ProfissionalSaude):
        pass

    def remover_profissional(self, p: ProfissionalSaude):
        pass

    def adicionar_atendimento(self, a: Atendimento):
        pass

    def remover_atendimento(self, a: Atendimento):
        pass

    def funcionaNoHorario(self, inicio: time, fim: time) -> bool:
        pass

    def totalAtendimentos(self) -> int:
        pass
