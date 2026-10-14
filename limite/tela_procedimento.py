from limite.tela import Tela


class TelaProcedimento(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- PROCEDIMENTOS ----------")
        print("1 - Incluir procedimento")
        print("2 - Alterar procedimento")
        print("3 - Excluir procedimento")
        print("4 - Listar procedimentos")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_procedimento(self) -> dict:
        print("\n-- Dados do procedimento --")
        return {
            "descricao": self.le_texto("Descrição: "),
            "custo": self.le_valor_decimal("Custo: "),
            "cpf_profissional": self.le_cpf("CPF do profissional responsável: "),
        }

    def pega_id(self) -> int:
        return self.le_num_inteiro("ID do procedimento: ")

    def pega_id_atendimento(self) -> int:
        return self.le_num_inteiro("ID do atendimento: ")

    def mostra_procedimento(self, dados: dict):
        print(f"\nProcedimento {dados['id']} (atendimento {dados['id_atendimento']})")
        print(f"Descrição: {dados['descricao']}")
        print(f"Custo: {self.formata_valor(dados['custo'])}")
        print(f"Profissional responsável: {dados['profissional']}")
