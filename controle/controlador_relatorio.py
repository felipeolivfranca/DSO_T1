from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_clinica import ControladorClinica
from limite.tela_relatorio import TelaRelatorio


class ControladorRelatorio:
    def __init__(self, controlador_clinica: ControladorClinica,
                 controlador_atendimento: ControladorAtendimento):
        self.__tela = TelaRelatorio()
        self.__controlador_clinica = controlador_clinica
        self.__controlador_atendimento = controlador_atendimento

    def clinicas_com_mais_atendimentos(self):
        pass

    def atendimentos_mais_caros_e_baratos(self):
        pass

    def procedimentos_mais_realizados(self):
        pass

    def procedimentos_mais_caros_e_baratos(self):
        pass

    def abrir_tela(self):
        pass
