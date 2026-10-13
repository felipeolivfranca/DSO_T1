from decimal import Decimal

from limite.tela import Tela


class TelaPagamento(Tela):
    def mostra_menu(self) -> int:
        pass

    def pega_forma(self) -> int:
        pass

    def pega_dados_pagamento(self) -> dict:
        pass

    def pega_dados_pix(self) -> dict:
        pass

    def pega_dados_cartao(self) -> dict:
        pass

    def pega_id(self) -> int:
        pass

    def mostra_pagamento(self, dados: dict):
        pass

    def mostra_valor_restante(self, valor: Decimal):
        pass
