import unittest

import dados_exemplo
from controle.controlador_principal import ControladorPrincipal
from testes.auxiliares import executar_ate_sair


class DadosExemploTest(unittest.TestCase):
    def iniciar_com_exemplo(self, entradas_do_usuario):
        def iniciar():
            dados_exemplo.ativar()
            ControladorPrincipal().iniciar()
        return executar_ate_sair(iniciar, entradas_do_usuario)

    def test_carrega_sem_erros_e_devolve_o_controle(self):
        codigo, saida = self.iniciar_com_exemplo(["0"])
        self.assertEqual(codigo, 0)
        self.assertIn("Dados de exemplo carregados", saida)
        self.assertNotIn("falha ao carregar", saida)
        self.assertIn("ATENDIMENTO EM CLÍNICAS", saida)

    def test_relatorios_com_os_dados_de_exemplo(self):
        _, saida = self.iniciar_com_exemplo(["8", "1", "2", "3", "4", "0", "0"])
        self.assertIn("1º Vida (Florianópolis): 3 atendimento(s)", saida)
        self.assertIn("Mais caro:  atendimento 3", saida)
        self.assertIn("1º Eletrocardiograma: 2 vez(es)", saida)
        self.assertIn("Mais barato: procedimento 6 - Nebulização", saida)


if __name__ == "__main__":
    unittest.main()
