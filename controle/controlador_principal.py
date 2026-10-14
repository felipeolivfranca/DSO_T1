import sys

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
        try:
            self.abrir_tela()
        except (KeyboardInterrupt, EOFError):
            self.encerrar()

    def abrir_tela(self):
        opcoes = {1: self.__abrir_tela_paciente, 2: self.__abrir_tela_profissional,
                  3: self.__abrir_tela_clinica, 4: self.__abrir_tela_tipo_atendimento,
                  5: self.__abrir_tela_atendimento, 6: self.__abrir_tela_procedimento,
                  7: self.__abrir_tela_pagamento, 8: self.__abrir_tela_relatorio}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                self.encerrar()
            try:
                opcoes[opcao]()
            except (KeyboardInterrupt, EOFError):
                raise
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def __abrir_tela_paciente(self):
        self.__controlador_paciente.abrir_tela()

    def __abrir_tela_profissional(self):
        self.__controlador_profissional.abrir_tela()

    def __abrir_tela_clinica(self):
        self.__controlador_clinica.abrir_tela()

    def __abrir_tela_tipo_atendimento(self):
        self.__controlador_tipo_atendimento.abrir_tela()

    def __abrir_tela_atendimento(self):
        self.__controlador_atendimento.abrir_tela()

    def __abrir_tela_procedimento(self):
        self.__controlador_procedimento.abrir_tela()

    def __abrir_tela_pagamento(self):
        self.__controlador_pagamento.abrir_tela()

    def __abrir_tela_relatorio(self):
        self.__controlador_relatorio.abrir_tela()

    def encerrar(self):
        self.__tela.mostra_mensagem("\nSistema encerrado. Até logo!")
        sys.exit(0)
