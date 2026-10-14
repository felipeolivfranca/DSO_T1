import unittest
from datetime import date, time
from decimal import Decimal

from limite.tela_pagamento import TelaPagamento
from limite.tela_principal import TelaPrincipal
from testes.auxiliares import executar


def ler(metodo, entradas):
    """Chama um método de leitura da tela e devolve (valor lido, texto impresso)."""
    resultado = {}
    saida = executar(lambda: resultado.setdefault("valor", metodo()), entradas)
    return resultado["valor"], saida


class TelaTest(unittest.TestCase):
    def setUp(self):
        self.tela = TelaPrincipal()

    def test_inteiro_repete_ate_valor_valido(self):
        valor, saida = ler(lambda: self.tela.le_num_inteiro("? ", [0, 1, 2]),
                           ["abc", "7", "2"])
        self.assertEqual(valor, 2)
        self.assertEqual(saida.count("Valor incorreto"), 2)

    def test_inteiro_sem_lista_de_validos(self):
        valor, _ = ler(lambda: self.tela.le_num_inteiro("? "), ["42"])
        self.assertEqual(valor, 42)

    def test_texto_nao_aceita_vazio(self):
        valor, saida = ler(lambda: self.tela.le_texto("? "), ["", "   ", "  Ana  "])
        self.assertEqual(valor, "Ana")
        self.assertEqual(saida.count("não pode ficar vazio"), 2)

    def test_decimal_aceita_virgula_e_rejeita_invalidos(self):
        valor, saida = ler(lambda: self.tela.le_valor_decimal("? "),
                           ["abc", "-5", "nan", "inf", "80,50"])
        self.assertEqual(valor, Decimal("80.50"))
        self.assertEqual(saida.count("Valor incorreto"), 4)

    def test_data(self):
        valor, saida = ler(lambda: self.tela.le_data("? "),
                           ["2026-10-20", "31/02/2026", "20/10/2026"])
        self.assertEqual(valor, date(2026, 10, 20))
        self.assertEqual(saida.count("Data inválida"), 2)

    def test_hora(self):
        valor, saida = ler(lambda: self.tela.le_hora("? "), ["25:00", "9h", "09:30"])
        self.assertEqual(valor, time(9, 30))
        self.assertEqual(saida.count("Horário inválido"), 2)

    def test_cpf_aceita_pontuacao_e_exige_11_numeros(self):
        valor, saida = ler(lambda: self.tela.le_cpf("? "),
                           ["123", "abcdefghijk", "111.222.333-44"])
        self.assertEqual(valor, "11122233344")
        self.assertEqual(saida.count("CPF inválido"), 2)

    def test_formatacao(self):
        self.assertEqual(self.tela.formata_valor(Decimal("1234.5")), "R$ 1.234,50")
        self.assertEqual(self.tela.formata_valor(Decimal("0")), "R$ 0,00")
        self.assertEqual(self.tela.formata_data(date(2026, 1, 5)), "05/01/2026")
        self.assertEqual(self.tela.formata_hora(time(8, 5)), "08:05")

    def test_menu_principal(self):
        valor, saida = ler(self.tela.mostra_menu, ["9", "8"])
        self.assertEqual(valor, 8)
        self.assertIn("Relatórios", saida)


class TelaPagamentoTest(unittest.TestCase):
    def test_numero_do_cartao(self):
        valor, saida = ler(TelaPagamento().pega_dados_cartao,
                           ["123", "4111 1111 1111 1111", "Visa"])
        self.assertEqual(valor, {"numero_cartao": "4111111111111111", "bandeira": "Visa"})
        self.assertIn("Número de cartão inválido", saida)

    def test_dados_sem_atendimento(self):
        valor, _ = ler(lambda: TelaPagamento().pega_dados_pagamento(com_atendimento=False),
                       ["19/10/2026", "50"])
        self.assertEqual(valor, {"data": date(2026, 10, 19), "valor_pago": Decimal("50")})


if __name__ == "__main__":
    unittest.main()
