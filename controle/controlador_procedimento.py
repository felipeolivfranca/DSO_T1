from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_profissional import ControladorProfissional
from entidade.procedimento import Procedimento
from limite.tela_procedimento import TelaProcedimento


class ControladorProcedimento:
    def __init__(self, controlador_atendimento: ControladorAtendimento,
                 controlador_profissional: ControladorProfissional):
        self.__tela = TelaProcedimento()
        self.__proximo_id = 1
        self.__controlador_atendimento = controlador_atendimento
        self.__controlador_profissional = controlador_profissional

    def incluir_procedimento(self):
        pass

    def alterar_procedimento(self):
        pass

    def excluir_procedimento(self):
        pass

    def listar_procedimento(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_id(self, id: int) -> Procedimento:
        pass
