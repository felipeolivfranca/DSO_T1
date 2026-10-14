from limite.tela import Tela


class TelaRelatorio(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- RELATÓRIOS ----------")
        print("1 - Clínicas com maior número de atendimentos")
        print("2 - Atendimentos mais caros e mais baratos")
        print("3 - Procedimentos mais realizados")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def mostra_ranking_clinicas(self, ranking: list):
        print("\n-- Clínicas com maior número de atendimentos --")
        for posicao, item in enumerate(ranking, start=1):
            print(f"{posicao}º {item['nome']} ({item['cidade']}): "
                  f"{item['total']} atendimento(s)")

    def mostra_extremos_atendimentos(self, maior: dict, menor: dict):
        print("\n-- Atendimentos mais caros e mais baratos --")
        print("Mais caro:  " + self.__descreve_atendimento(maior))
        print("Mais barato: " + self.__descreve_atendimento(menor))

    def mostra_ranking_procedimentos(self, ranking: list):
        print("\n-- Procedimentos mais realizados --")
        for posicao, item in enumerate(ranking, start=1):
            print(f"{posicao}º {item['descricao']}: {item['quantidade']} vez(es)")

    def mostra_extremos_procedimentos(self, maior: dict, menor: dict):
        print("\n-- Procedimentos mais caros e mais baratos --")
        print("Mais caro:  " + self.__descreve_procedimento(maior))
        print("Mais barato: " + self.__descreve_procedimento(menor))

    def __descreve_atendimento(self, dados: dict) -> str:
        return (f"atendimento {dados['id']} - {dados['paciente']} na clínica "
                f"{dados['clinica']} em {self.formata_data(dados['data'])}: "
                f"{self.formata_valor(dados['valor_total'])}")

    def __descreve_procedimento(self, dados: dict) -> str:
        return (f"procedimento {dados['id']} - {dados['descricao']} "
                f"(atendimento {dados['id_atendimento']}, {dados['profissional']}): "
                f"{self.formata_valor(dados['custo'])}")
