import io
from contextlib import redirect_stdout
from unittest.mock import patch

from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_clinica import ControladorClinica
from controle.controlador_paciente import ControladorPaciente
from controle.controlador_pagamento import ControladorPagamento
from controle.controlador_procedimento import ControladorProcedimento
from controle.controlador_profissional import ControladorProfissional
from controle.controlador_relatorio import ControladorRelatorio
from controle.controlador_tipo_atendimento import ControladorTipoAtendimento

CPF_JOAO = "11111111111"     # paciente adulto
CPF_BIA = "22222222222"      # paciente menor de idade em 20/10/2026
CPF_CAIO = "44444444444"     # paciente menor de idade
CPF_ANA = "33333333333"      # profissional
CPF_BETO = "55555555555"     # profissional
DATA_ATENDIMENTO = "20/10/2026"


def executar(funcao, entradas: list) -> str:
    """Executa a função simulando o que o usuário digita e devolve o que foi impresso."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
        funcao()
    return saida.getvalue()


def executar_ate_sair(funcao, entradas: list) -> tuple[int, str]:
    """Como executar(), para funções que encerram o programa; devolve (código, saída)."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
        try:
            funcao()
        except SystemExit as e:
            return e.code, saida.getvalue()
    raise AssertionError("O sistema deveria ter sido encerrado")


class Sistema:
    """Monta os controladores do mesmo jeito que o ControladorPrincipal."""

    def __init__(self):
        self.pacientes = ControladorPaciente()
        self.profissionais = ControladorProfissional()
        self.clinicas = ControladorClinica(self.profissionais)
        self.tipos = ControladorTipoAtendimento()
        self.atendimentos = ControladorAtendimento(self.pacientes, self.profissionais,
                                                   self.tipos, self.clinicas)
        self.procedimentos = ControladorProcedimento(self.atendimentos, self.profissionais)
        self.pagamentos = ControladorPagamento(self.atendimentos)
        self.relatorios = ControladorRelatorio(self.clinicas, self.atendimentos)

    def cadastrar_paciente(self, nome, cpf, nascimento):
        executar(self.pacientes.incluir_paciente, [nome, "48999990000", cpf, nascimento])

    def cadastrar_profissional(self, nome, cpf, registro):
        executar(self.profissionais.incluir_profissional,
                 [nome, "48988880000", cpf, "01/01/1980", "Cardiologia", registro])

    def cadastrar_clinica(self, nome, abertura="08:00", fechamento="18:00"):
        executar(self.clinicas.incluir_clinica,
                 [nome, "Florianópolis", "Clínica geral", abertura, fechamento])

    def vincular(self, clinica, cpf_profissional):
        executar(self.clinicas.vincular_profissional, [clinica, cpf_profissional])

    def cadastrar_atendimento(self, clinica, cpf_paciente, cpf_profissional=CPF_ANA,
                              inicio="09:00", fim="10:00", tipo="Consulta", valor="100",
                              data=DATA_ATENDIMENTO, responsavel=None):
        entradas = [clinica, cpf_paciente, cpf_profissional, data, inicio, fim, tipo, valor]
        if responsavel:
            entradas.append(responsavel)
        executar(self.atendimentos.incluir_atendimento, entradas)

    def cadastrar_procedimento(self, id_atendimento, descricao, custo,
                               cpf_profissional=CPF_ANA):
        executar(self.procedimentos.incluir_procedimento,
                 [str(id_atendimento), descricao, custo, cpf_profissional])

    def pagar_dinheiro(self, id_atendimento, data, valor):
        executar(self.pagamentos.incluir_pagamento, ["1", str(id_atendimento), data, valor])

    def com_dados_basicos(self):
        """Pacientes, profissional Ana vinculada à clínica Vida (08h às 18h)."""
        self.cadastrar_paciente("João", CPF_JOAO, "01/01/1990")
        self.cadastrar_paciente("Bia", CPF_BIA, "21/10/2010")
        self.cadastrar_paciente("Caio", CPF_CAIO, "01/01/2012")
        self.cadastrar_profissional("Ana", CPF_ANA, "CRM1")
        self.cadastrar_clinica("Vida")
        self.vincular("Vida", CPF_ANA)
        return self
