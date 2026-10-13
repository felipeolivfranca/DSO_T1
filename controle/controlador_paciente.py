from entidade.paciente import Paciente
from limite.tela_paciente import TelaPaciente


class ControladorPaciente:
    def __init__(self):
        self.__pacientes = []
        self.__tela_paciente = TelaPaciente()

    def incluir_paciente(self):
        pass

    def alterar_paciente(self):
        pass

    def excluir_paciente(self):
        pass

    def buscar_por_cpf(self, cpf: str) -> Paciente:
        pass

    def listar_paciente(self):
        pass

    def abrir_tela(self):
        pass
