from controle.controlador_clinica import ControladorClinica
from controle.controlador_paciente import ControladorPaciente
from controle.controlador_profissional import ControladorProfissional
from controle.controlador_tipo_atendimento import ControladorTipoAtendimento
from entidade.atendimento import Atendimento
from limite.tela_atendimento import TelaAtendimento


class ControladorAtendimento:
    def __init__(self, controlador_paciente: ControladorPaciente,
                 controlador_profissional: ControladorProfissional,
                 controlador_tipo_atendimento: ControladorTipoAtendimento,
                 controlador_clinica: ControladorClinica):
        self.__atendimentos = []
        self.__tela = TelaAtendimento()
        self.__proximo_id = 1
        self.__controlador_paciente = controlador_paciente
        self.__controlador_profissional = controlador_profissional
        self.__controlador_tipo_atendimento = controlador_tipo_atendimento
        self.__controlador_clinica = controlador_clinica

    def incluir_atendimento(self):
        pass

    def alterar_atendimento(self):
        pass

    def excluir_atendimento(self):
        pass

    def listar_atendimento(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_id(self, id: int) -> Atendimento:
        pass

    def __validar_idade_e_responsavel(self):
        pass

    def __validar_horario_clinica(self):
        pass
