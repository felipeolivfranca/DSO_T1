from limite.tela import Tela


class TelaPaciente(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- PACIENTES ----------")
        print("1 - Incluir paciente")
        print("2 - Alterar paciente")
        print("3 - Excluir paciente")
        print("4 - Listar pacientes")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_paciente(self) -> dict:
        print("\n-- Dados do paciente --")
        return {
            "nome": self.le_texto("Nome: "),
            "celular": self.le_texto("Celular: "),
            "cpf": self.le_cpf("CPF: "),
            "data_nascimento": self.le_data("Data de nascimento (dd/mm/aaaa): "),
        }

    def pega_cpf(self) -> str:
        return self.le_cpf("CPF do paciente: ")

    def mostra_paciente(self, dados: dict):
        print(f"\nNome: {dados['nome']}")
        print(f"CPF: {dados['cpf']}")
        print(f"Celular: {dados['celular']}")
        print(f"Nascimento: {self.formata_data(dados['data_nascimento'])} "
              f"({dados['idade']} anos)")
