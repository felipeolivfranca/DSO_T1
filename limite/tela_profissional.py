from limite.tela import Tela


class TelaProfissional(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- PROFISSIONAIS DE SAÚDE ----------")
        print("1 - Incluir profissional")
        print("2 - Alterar profissional")
        print("3 - Excluir profissional")
        print("4 - Listar profissionais")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_profissional(self) -> dict:
        print("\n-- Dados do profissional --")
        return {
            "nome": self.le_texto("Nome: "),
            "celular": self.le_texto("Celular: "),
            "cpf": self.le_cpf("CPF: "),
            "data_nascimento": self.le_data("Data de nascimento (dd/mm/aaaa): "),
            "especialidade": self.le_texto("Especialidade: "),
            "registro_profissional": self.le_texto("Registro profissional (ex.: CRM): "),
        }

    def pega_cpf(self) -> str:
        return self.le_cpf("CPF do profissional: ")

    def mostra_profissional(self, dados: dict):
        print(f"\nNome: {dados['nome']}")
        print(f"CPF: {dados['cpf']}")
        print(f"Celular: {dados['celular']}")
        print(f"Nascimento: {self.formata_data(dados['data_nascimento'])}")
        print(f"Especialidade: {dados['especialidade']}")
        print(f"Registro profissional: {dados['registro_profissional']}")
