from limite.tela import Tela


class TelaPrincipal(Tela):
    def mostra_menu(self) -> int:
        print("\n========== ATENDIMENTO EM CLÍNICAS ==========")
        print("1 - Pacientes")
        print("2 - Profissionais de saúde")
        print("3 - Clínicas")
        print("4 - Tipos de atendimento")
        print("5 - Atendimentos")
        print("6 - Procedimentos")
        print("7 - Pagamentos")
        print("8 - Relatórios")
        print("0 - Sair")
        return self.le_num_inteiro("Escolha a opção: ", list(range(9)))
