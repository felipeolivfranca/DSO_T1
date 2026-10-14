from decimal import Decimal

from limite.tela import Tela


class TelaPagamento(Tela):
    DINHEIRO = 1
    PIX = 2
    CARTAO = 3

    def mostra_menu(self) -> int:
        print("\n---------- PAGAMENTOS ----------")
        print("1 - Incluir pagamento")
        print("2 - Alterar pagamento")
        print("3 - Excluir pagamento")
        print("4 - Listar pagamentos")
        print("5 - Consultar valor restante de um atendimento")
        print("0 - Voltar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def pega_forma(self) -> int:
        print("\nForma de pagamento:")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de crédito")
        return self.le_num_inteiro("Escolha a forma: ", [self.DINHEIRO, self.PIX, self.CARTAO])

    def pega_dados_pagamento(self, com_atendimento: bool = True) -> dict:
        print("\n-- Dados do pagamento --")
        dados = {}
        if com_atendimento:
            dados["id_atendimento"] = self.le_num_inteiro("ID do atendimento: ")
        dados["data"] = self.le_data("Data do pagamento (dd/mm/aaaa): ")
        dados["valor_pago"] = self.le_valor_decimal("Valor pago: ")
        return dados

    def pega_dados_pix(self) -> dict:
        return {"cpf_pagador": self.le_cpf("CPF do pagador: ")}

    def pega_dados_cartao(self) -> dict:
        while True:
            numero = input("Número do cartão: ").strip().replace(" ", "")
            if numero.isdigit() and 13 <= len(numero) <= 19:
                break
            print("Número de cartão inválido! Digite de 13 a 19 números.")
        return {"numero_cartao": numero, "bandeira": self.le_texto("Bandeira: ")}

    def pega_id(self, mensagem: str = "ID do pagamento: ") -> int:
        return self.le_num_inteiro(mensagem)

    def mostra_pagamento(self, dados: dict):
        print(f"\nPagamento {dados['id']} - {dados['forma']}")
        print(f"Atendimento: {dados['id_atendimento']} | Paciente: {dados['paciente']}")
        print(f"Data: {self.formata_data(dados['data'])}")
        print(f"Valor pago: {self.formata_valor(dados['valor_pago'])}")
        print(f"Restante do atendimento: {self.formata_valor(dados['restante'])}")

    def mostra_valor_restante(self, valor: Decimal):
        if valor <= 0:
            print("Atendimento quitado.")
        else:
            print(f"Valor restante: {self.formata_valor(valor)}")
