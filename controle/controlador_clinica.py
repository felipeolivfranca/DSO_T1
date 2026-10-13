from controle.controlador_profissional import ControladorProfissional
from entidade.clinica import Clinica
from limite.tela_clinica import TelaClinica


class ControladorClinica:
    def __init__(self, controlador_profissional: ControladorProfissional):
        self.__clinicas = []
        self.__tela = TelaClinica()
        self.__controlador_profissional = controlador_profissional

    def incluir_clinica(self):
        pass

    def alterar_clinica(self):
        pass

    def excluir_clinica(self):
        pass

    def listar_clinica(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_nome(self, nome: str) -> Clinica:
        pass

    def vincular_profissional(self):
        pass

    def desvincular_profissional(self):
        pass
