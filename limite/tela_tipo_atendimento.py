from limite.tela import Tela


class TelaTipoAtendimento(Tela):
    def mostra_menu(self) -> int:
        print("\n---------- TIPOS DE ATENDIMENTO ----------")
        print("1 - Incluir tipo")
        print("2 - Alterar tipo")
        print("3 - Excluir tipo")
        print("4 - Listar tipos")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_tipo(self) -> dict:
        print("\n-- Dados do tipo de atendimento --")
        return {"descricao": self.le_texto("Descrição (ex.: consulta, exame, retorno): ")}

    def pega_descricao(self) -> str:
        return self.le_texto("Descrição do tipo de atendimento: ")

    def mostra_tipo(self, dados: dict):
        print(f"- {dados['descricao']}")
