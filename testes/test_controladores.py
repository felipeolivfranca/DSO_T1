import unittest
from decimal import Decimal
from unittest.mock import patch

from controle.controlador_paciente import ControladorPaciente
from controle.controlador_principal import ControladorPrincipal
from entidade.pagamento_cartao_credito import PagamentoCartaoCredito
from entidade.pagamento_pix import PagamentoPix
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.operacao_invalida_exception import OperacaoInvalidaException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException
from testes.auxiliares import (CPF_ANA, CPF_BETO, CPF_BIA, CPF_CAIO, CPF_JOAO,
                               DATA_ATENDIMENTO, Sistema, executar, executar_ate_sair)


class ControladorPacienteTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema()
        self.sistema.cadastrar_paciente("João", CPF_JOAO, "01/01/1990")
        self.controlador = self.sistema.pacientes

    def test_incluir(self):
        self.assertEqual(self.controlador.buscar_por_cpf(CPF_JOAO).nome, "João")

    def test_cpf_duplicado(self):
        with self.assertRaises(JaCadastradoException):
            executar(self.controlador.incluir_paciente, ["Outro", "1", CPF_JOAO, "01/01/2000"])

    def test_alterar(self):
        executar(self.controlador.alterar_paciente,
                 [CPF_JOAO, "João Silva", "4890", CPF_CAIO, "02/02/1991"])
        paciente = self.controlador.buscar_por_cpf(CPF_CAIO)
        self.assertEqual(paciente.nome, "João Silva")
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_cpf(CPF_JOAO)

    def test_alterar_para_cpf_de_outro_paciente(self):
        self.sistema.cadastrar_paciente("Bia", CPF_BIA, "21/10/2010")
        with self.assertRaises(JaCadastradoException):
            executar(self.controlador.alterar_paciente,
                     [CPF_JOAO, "João", "1", CPF_BIA, "01/01/1990"])

    def test_excluir(self):
        executar(self.controlador.excluir_paciente, [CPF_JOAO])
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_cpf(CPF_JOAO)

    def test_listar(self):
        saida = executar(self.controlador.listar_paciente, [])
        self.assertIn("João", saida)
        executar(self.controlador.excluir_paciente, [CPF_JOAO])
        self.assertIn("Nenhum paciente", executar(self.controlador.listar_paciente, []))

    def test_menu_mostra_erro_e_continua(self):
        saida = executar(self.controlador.abrir_tela,
                         ["1", "Outro", "1", CPF_JOAO, "01/01/2000", "3", CPF_BIA, "0"])
        self.assertIn("Já existe um paciente", saida)
        self.assertIn("não encontrado", saida)


class ControladorProfissionalTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema()
        self.sistema.cadastrar_profissional("Ana", CPF_ANA, "CRM1")
        self.controlador = self.sistema.profissionais

    def test_registro_duplicado_ignora_maiusculas(self):
        with self.assertRaises(JaCadastradoException):
            executar(self.controlador.incluir_profissional,
                     ["Beto", "1", CPF_BETO, "01/01/1985", "Orto", "crm1"])

    def test_alterar_mantendo_o_proprio_registro(self):
        executar(self.controlador.alterar_profissional,
                 [CPF_ANA, "Ana", "1", CPF_ANA, "01/01/1980", "Pediatria", "CRM1"])
        self.assertEqual(self.controlador.buscar_por_cpf(CPF_ANA).especialidade, "Pediatria")

    def test_excluir(self):
        executar(self.controlador.excluir_profissional, [CPF_ANA])
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_cpf(CPF_ANA)


class ControladorClinicaTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema().com_dados_basicos()
        self.controlador = self.sistema.clinicas

    def test_busca_ignora_maiusculas(self):
        self.assertEqual(self.controlador.buscar_por_nome("VIDA").nome, "Vida")

    def test_nome_duplicado(self):
        with self.assertRaises(JaCadastradoException):
            executar(self.controlador.incluir_clinica, ["vida", "F", "d", "08:00", "18:00"])

    def test_vincular_duas_vezes_e_desvincular(self):
        with self.assertRaises(JaCadastradoException):
            self.sistema.vincular("Vida", CPF_ANA)
        executar(self.controlador.desvincular_profissional, ["Vida", CPF_ANA])
        self.assertEqual(self.controlador.buscar_por_nome("Vida").profissionais, [])
        with self.assertRaises(NaoEncontradoException):
            executar(self.controlador.desvincular_profissional, ["Vida", CPF_ANA])

    def test_alterar(self):
        executar(self.controlador.alterar_clinica,
                 ["Vida", "Vida Nova", "Joinville", "Nova", "07:00", "19:00"])
        clinica = self.controlador.buscar_por_nome("Vida Nova")
        self.assertEqual(clinica.cidade, "Joinville")

    def test_nao_exclui_clinica_com_atendimentos(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        with self.assertRaises(OperacaoInvalidaException):
            executar(self.controlador.excluir_clinica, ["Vida"])

    def test_excluir(self):
        executar(self.controlador.excluir_clinica, ["Vida"])
        self.assertEqual(self.controlador.clinicas, [])


class ControladorTipoAtendimentoTest(unittest.TestCase):
    def setUp(self):
        self.controlador = Sistema().tipos

    def test_tipos_iniciais(self):
        for descricao in ("consulta", "Exame", "RETORNO"):
            self.controlador.buscar_por_descricao(descricao)

    def test_incluir_duplicado(self):
        with self.assertRaises(JaCadastradoException):
            executar(self.controlador.incluir_tipo_atendimento, ["CONSULTA"])

    def test_alterar_e_excluir(self):
        executar(self.controlador.alterar_tipo_atendimento, ["Retorno", "Revisão"])
        self.assertEqual(self.controlador.buscar_por_descricao("revisão").descricao, "Revisão")
        executar(self.controlador.excluir_tipo_atendimento, ["Revisão"])
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_descricao("Revisão")


class ControladorAtendimentoTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema().com_dados_basicos()
        self.controlador = self.sistema.atendimentos

    def test_incluir(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        atendimento = self.controlador.buscar_por_id(1)
        self.assertEqual(atendimento.paciente.nome, "João")
        self.assertIsNone(atendimento.responsavel)
        self.assertEqual(self.sistema.clinicas.buscar_por_nome("Vida").totalAtendimentos(), 1)

    def test_ids_sao_sequenciais(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, inicio="10:00", fim="11:00")
        self.assertEqual([a.id for a in self.controlador.atendimentos], [1, 2])

    def test_profissional_nao_vinculado_a_clinica(self):
        self.sistema.cadastrar_profissional("Beto", CPF_BETO, "CRM2")
        with self.assertRaises(OperacaoInvalidaException):
            self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, cpf_profissional=CPF_BETO)

    def test_fora_do_horario_da_clinica(self):
        with self.assertRaises(OperacaoInvalidaException):
            self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, inicio="17:00", fim="19:00")

    def test_inicio_igual_ao_fim(self):
        with self.assertRaises(OperacaoInvalidaException):
            self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, inicio="09:00", fim="09:00")

    def test_menor_com_responsavel_adulto(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel=CPF_JOAO)
        self.assertEqual(self.controlador.buscar_por_id(1).responsavel.nome, "João")

    def test_responsavel_pode_ser_profissional(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel=CPF_ANA)
        self.assertEqual(self.controlador.buscar_por_id(1).responsavel.nome, "Ana")

    def test_responsavel_menor_de_idade(self):
        with self.assertRaises(OperacaoInvalidaException):
            self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel=CPF_CAIO)

    def test_paciente_como_proprio_responsavel(self):
        with self.assertRaises(OperacaoInvalidaException):
            self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel=CPF_BIA)

    def test_responsavel_nao_cadastrado(self):
        with self.assertRaises(NaoEncontradoException):
            self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel="99999999999")

    def test_paciente_ou_tipo_inexistente(self):
        with self.assertRaises(NaoEncontradoException):
            self.sistema.cadastrar_atendimento("Vida", "99999999999")
        with self.assertRaises(NaoEncontradoException):
            self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, tipo="Cirurgia")

    def test_alterar_trocando_de_clinica(self):
        self.sistema.cadastrar_clinica("Noite", "22:00", "06:00")
        self.sistema.vincular("Noite", CPF_ANA)
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        executar(self.controlador.alterar_atendimento,
                 ["1", "Noite", CPF_JOAO, CPF_ANA, DATA_ATENDIMENTO, "23:00", "01:00",
                  "Exame", "150"])
        atendimento = self.controlador.buscar_por_id(1)
        self.assertEqual(atendimento.clinica.nome, "Noite")
        self.assertEqual(atendimento.valor, Decimal("150"))
        self.assertEqual(self.sistema.clinicas.buscar_por_nome("Vida").totalAtendimentos(), 0)
        self.assertEqual(self.sistema.clinicas.buscar_por_nome("Noite").totalAtendimentos(), 1)

    def test_alterar_data_para_antes_de_um_pagamento(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "50")
        with self.assertRaises(OperacaoInvalidaException):
            executar(self.controlador.alterar_atendimento,
                     ["1", "Vida", CPF_JOAO, CPF_ANA, "19/10/2026", "09:00", "10:00",
                      "Consulta", "100"])

    def test_excluir(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        executar(self.controlador.excluir_atendimento, ["1"])
        self.assertEqual(self.controlador.atendimentos, [])
        self.assertEqual(self.sistema.clinicas.buscar_por_nome("Vida").totalAtendimentos(), 0)

    def test_nao_exclui_atendimento_com_pagamentos(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "50")
        with self.assertRaises(OperacaoInvalidaException):
            executar(self.controlador.excluir_atendimento, ["1"])

    def test_listar(self):
        self.sistema.cadastrar_atendimento("Vida", CPF_BIA, responsavel=CPF_JOAO)
        saida = executar(self.controlador.listar_atendimento, [])
        self.assertIn("Responsável: João", saida)
        self.assertIn("Restante: R$ 100,00", saida)


class ControladorProcedimentoTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema().com_dados_basicos()
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO)
        self.sistema.cadastrar_procedimento(1, "ECG", "50")
        self.controlador = self.sistema.procedimentos
        self.atendimento = self.sistema.atendimentos.buscar_por_id(1)

    def test_incluir(self):
        self.assertEqual(self.controlador.buscar_por_id(1).descricao, "ECG")
        self.assertEqual(self.atendimento.calcularValorTotal(), Decimal("150"))

    def test_incluir_em_atendimento_inexistente(self):
        with self.assertRaises(NaoEncontradoException):
            self.sistema.cadastrar_procedimento(99, "ECG", "50")

    def test_alterar(self):
        executar(self.controlador.alterar_procedimento, ["1", "ECG completo", "70", CPF_ANA])
        self.assertEqual(self.atendimento.calcularValorTotal(), Decimal("170"))

    def test_excluir(self):
        executar(self.controlador.excluir_procedimento, ["1"])
        self.assertEqual(self.atendimento.procedimentos, [])
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_id(1)


class ControladorPagamentoTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema().com_dados_basicos()
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, valor="150")
        self.controlador = self.sistema.pagamentos
        self.atendimento = self.sistema.atendimentos.buscar_por_id(1)

    def test_pagamentos_parciais_nas_tres_formas(self):
        self.sistema.pagar_dinheiro(1, "18/10/2026", "50")
        executar(self.controlador.incluir_pagamento,
                 ["2", "1", "19/10/2026", "50", CPF_JOAO])
        saida = executar(self.controlador.incluir_pagamento,
                         ["3", "1", DATA_ATENDIMENTO, "50", "4111111111111111", "Visa"])
        self.assertIsInstance(self.controlador.buscar_por_id(2), PagamentoPix)
        self.assertIsInstance(self.controlador.buscar_por_id(3), PagamentoCartaoCredito)
        self.assertTrue(self.atendimento.estaQuitado())
        self.assertIn("Atendimento quitado", saida)

    def test_pagamento_depois_do_atendimento(self):
        with self.assertRaises(PagamentoInvalidoException):
            self.sistema.pagar_dinheiro(1, "21/10/2026", "50")

    def test_pagamento_maior_que_o_restante(self):
        with self.assertRaises(PagamentoInvalidoException):
            self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "150,01")

    def test_alterar_considera_o_valor_antigo(self):
        self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "100")
        executar(self.controlador.alterar_pagamento, ["1", DATA_ATENDIMENTO, "150"])
        self.assertTrue(self.atendimento.estaQuitado())
        with self.assertRaises(PagamentoInvalidoException):
            executar(self.controlador.alterar_pagamento, ["1", DATA_ATENDIMENTO, "151"])

    def test_alterar_dados_do_pix(self):
        executar(self.controlador.incluir_pagamento, ["2", "1", DATA_ATENDIMENTO, "50", CPF_JOAO])
        executar(self.controlador.alterar_pagamento, ["1", DATA_ATENDIMENTO, "60", CPF_BIA])
        pagamento = self.controlador.buscar_por_id(1)
        self.assertEqual(pagamento.cpf_pagador, CPF_BIA)
        self.assertEqual(pagamento.valor_pago, Decimal("60"))

    def test_excluir_devolve_o_valor_ao_restante(self):
        self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "100")
        executar(self.controlador.excluir_pagamento, ["1"])
        self.assertEqual(self.atendimento.calcularTotalRestante(), Decimal("150"))
        with self.assertRaises(NaoEncontradoException):
            self.controlador.buscar_por_id(1)

    def test_consultar_valor_restante(self):
        self.sistema.pagar_dinheiro(1, DATA_ATENDIMENTO, "40")
        saida = executar(self.controlador.consultar_valor_restante, ["1"])
        self.assertIn("R$ 110,00", saida)


class ControladorRelatorioTest(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema().com_dados_basicos()
        self.controlador = self.sistema.relatorios

    def test_relatorios_sem_dados(self):
        for relatorio in (self.controlador.atendimentos_mais_caros_e_baratos,
                          self.controlador.procedimentos_mais_realizados,
                          self.controlador.procedimentos_mais_caros_e_baratos):
            with self.assertRaises(NaoEncontradoException):
                executar(relatorio, [])

    def test_relatorios(self):
        self.sistema.cadastrar_clinica("Noite", "22:00", "06:00")
        self.sistema.vincular("Noite", CPF_ANA)
        self.sistema.cadastrar_atendimento("Noite", CPF_JOAO, inicio="23:00", fim="00:00",
                                           valor="100")
        self.sistema.cadastrar_atendimento("Noite", CPF_JOAO, inicio="01:00", fim="02:00",
                                           valor="300")
        self.sistema.cadastrar_atendimento("Vida", CPF_JOAO, valor="200")
        self.sistema.cadastrar_procedimento(1, "ECG", "30")
        self.sistema.cadastrar_procedimento(2, "ecg", "40")
        self.sistema.cadastrar_procedimento(3, "Raio-X", "80,50")

        saida = executar(self.controlador.clinicas_com_mais_atendimentos, [])
        self.assertLess(saida.index("1º Noite"), saida.index("2º Vida"))

        saida = executar(self.controlador.atendimentos_mais_caros_e_baratos, [])
        self.assertIn("Mais caro:  atendimento 2", saida)
        self.assertIn("R$ 340,00", saida)
        self.assertIn("Mais barato: atendimento 1", saida)

        saida = executar(self.controlador.procedimentos_mais_realizados, [])
        self.assertIn("1º ECG: 2 vez(es)", saida)
        self.assertIn("2º Raio-X: 1 vez(es)", saida)

        saida = executar(self.controlador.procedimentos_mais_caros_e_baratos, [])
        self.assertIn("Mais caro:  procedimento 3 - Raio-X", saida)
        self.assertIn("Mais barato: procedimento 1 - ECG", saida)

    def test_menu_mostra_aviso_sem_dados(self):
        saida = executar(self.controlador.abrir_tela, ["2", "0"])
        self.assertIn("Não há dados para o relatório", saida)


class ControladorPrincipalTest(unittest.TestCase):
    def test_sair_pelo_menu(self):
        codigo, saida = executar_ate_sair(ControladorPrincipal().iniciar, ["0"])
        self.assertEqual(codigo, 0)
        self.assertIn("Sistema encerrado", saida)

    def test_fim_da_entrada_encerra_o_sistema(self):
        codigo, saida = executar_ate_sair(ControladorPrincipal().iniciar,
                                          ["1", "4", EOFError()])
        self.assertEqual(codigo, 0)
        self.assertIn("Sistema encerrado", saida)

    def test_ctrl_c_encerra_o_sistema(self):
        codigo, _ = executar_ate_sair(ControladorPrincipal().iniciar, [KeyboardInterrupt()])
        self.assertEqual(codigo, 0)

    def test_navega_por_todos_os_menus(self):
        entradas = ["1", "4", "0", "2", "4", "0", "3", "4", "0", "4", "4", "0",
                    "5", "4", "0", "6", "4", "0", "7", "4", "0", "8", "1", "0", "0"]
        codigo, saida = executar_ate_sair(ControladorPrincipal().iniciar, entradas)
        self.assertEqual(codigo, 0)
        self.assertNotIn("Erro inesperado", saida)
        for titulo in ("PACIENTES", "PROFISSIONAIS", "CLÍNICAS", "TIPOS DE ATENDIMENTO",
                       "ATENDIMENTOS", "PROCEDIMENTOS", "PAGAMENTOS", "RELATÓRIOS"):
            self.assertIn(titulo, saida)

    def test_erro_inesperado_nao_derruba_o_sistema(self):
        with patch.object(ControladorPaciente, "abrir_tela",
                          side_effect=ZeroDivisionError("falha simulada")):
            codigo, saida = executar_ate_sair(ControladorPrincipal().iniciar, ["1", "0"])
        self.assertEqual(codigo, 0)
        self.assertIn("Erro inesperado: falha simulada", saida)


if __name__ == "__main__":
    unittest.main()
