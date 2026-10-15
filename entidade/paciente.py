from datetime import date

from entidade.pessoa import Pessoa


class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        super().__init__(nome, celular, cpf, data_nascimento)

    def obter_papel(self) -> str:
        return "Paciente"
