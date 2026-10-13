from abc import ABC, abstractmethod
from datetime import date


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        self.__nome = nome
        self.__celular = celular
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        self.__celular = celular

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        self.__data_nascimento = data_nascimento

    def calcularIdade(self, dataReferencia: date) -> int:
        pass

    def ehMaiorDeIdade(self, dataReferencia: date) -> bool:
        pass

    @abstractmethod
    def obterPapel(self) -> str:
        pass
