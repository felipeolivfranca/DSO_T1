from limite.tela import Tela


class TelaAtendimento(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- ATENDIMENTOS ----------")
        print("1 - Incluir atendimento")
        print("2 - Alterar atendimento")
        print("3 - Excluir atendimento")
        print("4 - Listar atendimentos")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_atendimento(self) -> dict:
        print("\n-- Dados do atendimento --")
        return {
            "clinica": self.le_texto("Nome da clínica: "),
            "cpf_paciente": self.le_cpf("CPF do paciente: "),
            "cpf_profissional": self.le_cpf("CPF do profissional: "),
            "data": self.le_data("Data (dd/mm/aaaa): "),
            "horario_inicio": self.le_hora("Horário de início (hh:mm): "),
            "horario_fim": self.le_hora("Horário de fim (hh:mm): "),
            "tipo": self.le_texto("Tipo de atendimento: "),
            "valor": self.le_valor_decimal("Valor: "),
        }

    def pega_cpf_atendimento(self) -> str:
        return self.le_cpf("CPF do responsável (paciente ou profissional cadastrado): ")

    def pega_id(self) -> int:
        return self.le_num_inteiro("ID do atendimento: ")

    def mostra_atendimento(self, dados: dict):
        print(f"\nAtendimento {dados['id']} - {dados['tipo']}")
        print(f"Clínica: {dados['clinica']}")
        print(f"Paciente: {dados['paciente']}")
        if dados["responsavel"]:
            print(f"Responsável: {dados['responsavel']}")
        print(f"Profissional: {dados['profissional']}")
        print(f"Data: {self.formata_data(dados['data'])}, "
              f"{self.formata_hora(dados['horario_inicio'])} às "
              f"{self.formata_hora(dados['horario_fim'])}")
        procedimentos = ", ".join(dados["procedimentos"]) or "nenhum"
        print(f"Procedimentos: {procedimentos}")
        print(f"Valor do atendimento: {self.formata_valor(dados['valor'])}")
        print(f"Valor total (com procedimentos): {self.formata_valor(dados['valor_total'])}")
        print(f"Pago: {self.formata_valor(dados['total_pago'])} | "
              f"Restante: {self.formata_valor(dados['restante'])}"
              f"{' (quitado)' if dados['quitado'] else ''}")
