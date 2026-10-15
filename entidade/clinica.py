from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from entidade.profissional_saude import ProfissionalSaude
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException

if TYPE_CHECKING:
    from entidade.atendimento import Atendimento


class Clinica:
    __MINUTOS_DIA = 24 * 60

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

    def adicionar_profissional(self, profissional: ProfissionalSaude):
        if any(prof.registro_profissional == profissional.registro_profissional for prof in self.__profissionais):
            raise JaCadastradoException(
                f"{profissional.nome} já está vinculado à clínica {self.__nome}")
        self.__profissionais.append(profissional)

    def remover_profissional(self, profissional: ProfissionalSaude):
        for prof in self.__profissionais:
            if prof.registro_profissional == profissional.registro_profissional:
                self.__profissionais.remove(prof)
                return
        raise NaoEncontradoException(
            f"{profissional.nome} não está vinculado à clínica {self.__nome}")

    def adicionar_atendimento(self, atendimento: Atendimento):
        if any(atend.id == atendimento.id for atend in self.__atendimentos):
            raise JaCadastradoException(
                f"Atendimento {atendimento.id} já pertence à clínica {self.__nome}")
        self.__atendimentos.append(atendimento)

    def remover_atendimento(self, atendimento: Atendimento):
        for atend in self.__atendimentos:
            if atend.id == atendimento.id:
                self.__atendimentos.remove(atend)
                return
        raise NaoEncontradoException(
            f"Atendimento {atendimento.id} não pertence à clínica {self.__nome}")

    def funcionaNoHorario(self, inicio: time, fim: time) -> bool:
        # Trabalha em minutos desde 00:00; horários que passam da meia-noite
        # são deslocados para o "dia seguinte" (+24h).
        abertura = self.__em_minutos(self.__horario_abertura)
        fechamento = self.__em_minutos(self.__horario_fechamento)
        if abertura == fechamento:  # aberta 24h
            return True
        if fechamento < abertura:
            fechamento += self.__MINUTOS_DIA

        ini = self.__em_minutos(inicio)
        fim_min = self.__em_minutos(fim)
        if ini < abertura:
            ini += self.__MINUTOS_DIA
            fim_min += self.__MINUTOS_DIA
        if fim_min <= ini:
            fim_min += self.__MINUTOS_DIA

        return abertura <= ini and fim_min <= fechamento

    @staticmethod
    def __em_minutos(horario: time) -> int:
        return horario.hour * 60 + horario.minute

    def totalAtendimentos(self) -> int:
        return len(self.__atendimentos)
