from limite.tela import Tela


class TelaClinica(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- CLÍNICAS ----------")
        print("1 - Incluir clínica")
        print("2 - Alterar clínica")
        print("3 - Excluir clínica")
        print("4 - Listar clínicas")
        print("5 - Vincular profissional")
        print("6 - Desvincular profissional")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5, 6])

    def pega_dados_clinica(self) -> dict:
        print("\n-- Dados da clínica --")
        return {
            "nome": self.le_texto("Nome: "),
            "cidade": self.le_texto("Cidade: "),
            "descricao": self.le_texto("Descrição: "),
            "horario_abertura": self.le_hora("Horário de abertura (hh:mm): "),
            "horario_fechamento": self.le_hora("Horário de fechamento (hh:mm): "),
        }

    def pega_nome(self) -> str:
        return self.le_texto("Nome da clínica: ")

    def pega_cpf_profissional(self) -> str:
        return self.le_cpf("CPF do profissional: ")

    def mostra_clinica(self, dados: dict):
        print(f"\nNome: {dados['nome']}")
        print(f"Cidade: {dados['cidade']}")
        print(f"Descrição: {dados['descricao']}")
        print(f"Funcionamento: {self.formata_hora(dados['horario_abertura'])} às "
              f"{self.formata_hora(dados['horario_fechamento'])}")
        profissionais = ", ".join(dados["profissionais"]) or "nenhum"
        print(f"Profissionais: {profissionais}")
        print(f"Total de atendimentos: {dados['total_atendimentos']}")
