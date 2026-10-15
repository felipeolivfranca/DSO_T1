import unittest
from datetime import date, time
from decimal import Decimal

from entidade.atendimento import Atendimento
from entidade.clinica import Clinica
from entidade.paciente import Paciente
from entidade.pagamento import Pagamento
from entidade.pagamento_cartao_credito import PagamentoCartaoCredito
from entidade.pagamento_dinheiro import PagamentoDinheiro
from entidade.pagamento_pix import PagamentoPix
from entidade.pessoa import Pessoa
from entidade.procedimento import Procedimento
from entidade.profissional_saude import ProfissionalSaude
from entidade.tipo_atendimento import TipoAtendimento
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException

DIA = date(2026, 10, 20)


def novo_profissional(registro="CRM1", cpf="33333333333"):
    return ProfissionalSaude("Ana", "4899", cpf, date(1980, 1, 1), "Cardiologia", registro)


def novo_atendimento(valor="100", id=1, paciente=None):
    clinica = Clinica("Vida", "Florianópolis", "Geral", time(8), time(18))
    paciente = paciente or Paciente("João", "4899", "11111111111", date(1990, 1, 1))
    return Atendimento(clinica, paciente, novo_profissional(), DIA, time(9), time(10),
                       TipoAtendimento("Consulta"), Decimal(valor), id)


class PessoaTest(unittest.TestCase):
    def test_pessoa_e_abstrata(self):
        with self.assertRaises(TypeError):
            Pessoa("X", "1", "1", date(2000, 1, 1))

    def test_idade_antes_e_depois_do_aniversario(self):
        bia = Paciente("Bia", "1", "2", date(2008, 10, 21))
        self.assertEqual(bia.calcular_idade(date(2026, 10, 20)), 17)
        self.assertEqual(bia.calcular_idade(date(2026, 10, 21)), 18)

    def test_idade_de_quem_nasceu_em_29_de_fevereiro(self):
        pessoa = Paciente("Leo", "1", "2", date(2008, 2, 29))
        self.assertEqual(pessoa.calcular_idade(date(2026, 2, 28)), 17)
        self.assertEqual(pessoa.calcular_idade(date(2026, 3, 1)), 18)

    def test_maioridade_com_18_anos_completos(self):
        bia = Paciente("Bia", "1", "2", date(2008, 10, 21))
        self.assertFalse(bia.eh_maior_de_idade(date(2026, 10, 20)))
        self.assertTrue(bia.eh_maior_de_idade(date(2026, 10, 21)))

    def test_papeis(self):
        self.assertEqual(Paciente("P", "1", "2", DIA).obter_papel(), "Paciente")
        self.assertEqual(novo_profissional().obter_papel(), "Profissional de Saúde")

    def test_getters_e_setters(self):
        ana = novo_profissional()
        ana.nome = "Ana Souza"
        ana.especialidade = "Pediatria"
        self.assertEqual(ana.nome, "Ana Souza")
        self.assertEqual(ana.especialidade, "Pediatria")


class ClinicaTest(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica("Vida", "Florianópolis", "Geral", time(8), time(18))

    def test_adicionar_e_remover_profissional(self):
        ana = novo_profissional()
        self.clinica.adicionar_profissional(ana)
        self.assertIn(ana, self.clinica.profissionais)
        self.clinica.remover_profissional(ana)
        self.assertEqual(self.clinica.profissionais, [])

    def test_profissional_duplicado_pelo_registro(self):
        self.clinica.adicionar_profissional(novo_profissional())
        with self.assertRaises(JaCadastradoException):
            self.clinica.adicionar_profissional(novo_profissional(cpf="99999999999"))

    def test_remover_profissional_nao_vinculado(self):
        with self.assertRaises(NaoEncontradoException):
            self.clinica.remover_profissional(novo_profissional())

    def test_atendimentos(self):
        atendimento = novo_atendimento()
        self.clinica.adicionar_atendimento(atendimento)
        self.assertEqual(self.clinica.total_atendimentos(), 1)
        with self.assertRaises(JaCadastradoException):
            self.clinica.adicionar_atendimento(atendimento)
        self.clinica.remover_atendimento(atendimento)
        self.assertEqual(self.clinica.total_atendimentos(), 0)
        with self.assertRaises(NaoEncontradoException):
            self.clinica.remover_atendimento(atendimento)

    def test_horario_de_funcionamento_diurno(self):
        funciona = self.clinica.funciona_no_horario
        self.assertTrue(funciona(time(9), time(10)))
        self.assertTrue(funciona(time(8), time(18)))
        self.assertFalse(funciona(time(7), time(8)))
        self.assertFalse(funciona(time(17), time(19)))
        self.assertFalse(funciona(time(10), time(9)))

    def test_horario_que_passa_da_meia_noite(self):
        funciona = Clinica("Noite", "F", "d", time(22), time(6)).funciona_no_horario
        self.assertTrue(funciona(time(23), time(1)))
        self.assertTrue(funciona(time(1), time(2)))
        self.assertTrue(funciona(time(22), time(6)))
        self.assertFalse(funciona(time(12), time(13)))
        self.assertFalse(funciona(time(5), time(7)))

    def test_abertura_igual_ao_fechamento_funciona_24h(self):
        funciona = Clinica("24h", "F", "d", time(0), time(0)).funciona_no_horario
        self.assertTrue(funciona(time(3), time(4)))
        self.assertTrue(funciona(time(23), time(1)))


class AtendimentoTest(unittest.TestCase):
    def setUp(self):
        self.atendimento = novo_atendimento()
        self.ana = self.atendimento.profissional

    def test_procedimentos_entram_no_valor_total(self):
        self.atendimento.adicionar_procedimento(Procedimento("ECG", Decimal("50"), self.ana, 1))
        self.assertEqual(self.atendimento.calcular_valor_total(), Decimal("150"))

    def test_procedimento_duplicado_e_remocao(self):
        ecg = Procedimento("ECG", Decimal("50"), self.ana, 1)
        self.atendimento.adicionar_procedimento(ecg)
        with self.assertRaises(JaCadastradoException):
            self.atendimento.adicionar_procedimento(ecg)
        self.atendimento.remover_procedimento(ecg)
        with self.assertRaises(NaoEncontradoException):
            self.atendimento.remover_procedimento(ecg)

    def test_pagamento_parcial_e_quitacao(self):
        paciente = self.atendimento.paciente
        self.atendimento.adicionar_pagamento(
            PagamentoDinheiro(1, DIA, self.atendimento, paciente, Decimal("60")))
        self.assertEqual(self.atendimento.calcular_total_pago(), Decimal("60"))
        self.assertEqual(self.atendimento.calcular_total_restante(), Decimal("40"))
        self.assertFalse(self.atendimento.esta_quitado())
        self.atendimento.adicionar_pagamento(
            PagamentoDinheiro(2, DIA, self.atendimento, paciente, Decimal("40")))
        self.assertTrue(self.atendimento.esta_quitado())

    def test_pagamento_depois_da_data_do_atendimento(self):
        with self.assertRaises(PagamentoInvalidoException):
            self.atendimento.adicionar_pagamento(PagamentoDinheiro(
                1, date(2026, 10, 21), self.atendimento, self.atendimento.paciente,
                Decimal("10")))

    def test_pagamento_zerado_ou_maior_que_o_restante(self):
        paciente = self.atendimento.paciente
        with self.assertRaises(PagamentoInvalidoException):
            self.atendimento.adicionar_pagamento(
                PagamentoDinheiro(1, DIA, self.atendimento, paciente, Decimal("0")))
        with self.assertRaises(PagamentoInvalidoException):
            self.atendimento.adicionar_pagamento(
                PagamentoDinheiro(2, DIA, self.atendimento, paciente, Decimal("100.01")))

    def test_pagamento_duplicado_e_remocao(self):
        pagamento = PagamentoDinheiro(1, DIA, self.atendimento, self.atendimento.paciente,
                                      Decimal("10"))
        self.atendimento.adicionar_pagamento(pagamento)
        with self.assertRaises(JaCadastradoException):
            self.atendimento.adicionar_pagamento(pagamento)
        self.atendimento.remover_pagamento(pagamento)
        self.assertEqual(self.atendimento.calcular_total_pago(), Decimal("0"))
        with self.assertRaises(NaoEncontradoException):
            self.atendimento.remover_pagamento(pagamento)

    def test_paciente_menor(self):
        self.assertFalse(self.atendimento.paciente_eh_menor())
        menor = Paciente("Bia", "1", "2", date(2010, 10, 21))
        self.assertTrue(novo_atendimento(paciente=menor).paciente_eh_menor())


class PagamentoTest(unittest.TestCase):
    def setUp(self):
        self.atendimento = novo_atendimento()
        self.paciente = self.atendimento.paciente

    def test_pagamento_e_abstrato(self):
        with self.assertRaises(TypeError):
            Pagamento(1, DIA, self.atendimento, self.paciente, Decimal("10"))

    def test_descricao_das_formas(self):
        dinheiro = PagamentoDinheiro(1, DIA, self.atendimento, self.paciente, Decimal("10"))
        pix = PagamentoPix(2, DIA, self.atendimento, self.paciente, Decimal("10"), "123")
        cartao = PagamentoCartaoCredito(3, DIA, self.atendimento, self.paciente,
                                        Decimal("10"), "4111111111111234", "Visa")
        self.assertEqual(dinheiro.descrever_forma(), "Dinheiro")
        self.assertEqual(pix.descrever_forma(), "PIX (CPF do pagador: 123)")
        self.assertEqual(cartao.descrever_forma(), "Cartão de crédito Visa final 1234")

    def test_valor_restante_vem_do_atendimento(self):
        pix = PagamentoPix(1, DIA, self.atendimento, self.paciente, Decimal("30"), "123")
        self.atendimento.adicionar_pagamento(pix)
        self.assertEqual(pix.calcular_valor_restante(), Decimal("70"))


if __name__ == "__main__":
    unittest.main()
