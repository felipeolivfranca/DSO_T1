from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_clinica import ControladorClinica
from controle.controlador_paciente import ControladorPaciente
from controle.controlador_pagamento import ControladorPagamento
from controle.controlador_procedimento import ControladorProcedimento
from controle.controlador_profissional import ControladorProfissional
from controle.controlador_relatorio import ControladorRelatorio
from controle.controlador_tipo_atendimento import ControladorTipoAtendimento
from limite.tela_principal import TelaPrincipal


class ControladorPrincipal:
    def __init__(self):
        self.__tela = TelaPrincipal()
        self.__controlador_paciente = ControladorPaciente()
        self.__controlador_profissional = ControladorProfissional()
        self.__controlador_clinica = ControladorClinica(self.__controlador_profissional)
        self.__controlador_tipo_atendimento = ControladorTipoAtendimento()
        self.__controlador_atendimento = ControladorAtendimento(
            self.__controlador_paciente,
            self.__controlador_profissional,
            self.__controlador_tipo_atendimento,
            self.__controlador_clinica,
        )
        self.__controlador_procedimento = ControladorProcedimento(
            self.__controlador_atendimento,
            self.__controlador_profissional,
        )
        self.__controlador_pagamento = ControladorPagamento(self.__controlador_atendimento)
        self.__controlador_relatorio = ControladorRelatorio(
            self.__controlador_clinica,
            self.__controlador_atendimento,
        )

    def iniciar(self):
        pass

    def abrir_tela(self):
        pass

    def __abrir_tela_paciente(self):
        pass

    def __abrir_tela_profissional(self):
        pass

    def __abrir_tela_clinica(self):
        pass

    def __abrir_tela_tipo_atendimento(self):
        pass

    def __abrir_tela_atendimento(self):
        pass

    def __abrir_tela_procedimento(self):
        pass

    def __abrir_tela_pagamento(self):
        pass

    def __abrir_tela_relatorio(self):
        pass

    def encerrar(self):
        pass
