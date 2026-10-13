from controle.controlador_atendimento import ControladorAtendimento
from entidade.pagamento import Pagamento
from limite.tela_pagamento import TelaPagamento


class ControladorPagamento:
    def __init__(self, controlador_atendimento: ControladorAtendimento):
        self.__pagamentos = []
        self.__tela = TelaPagamento()
        self.__proximo_id = 1
        self.__controlador_atendimento = controlador_atendimento

    def incluir_pagamento(self):
        pass

    def alterar_pagamento(self):
        pass

    def excluir_pagamento(self):
        pass

    def listar_pagamento(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_id(self, id: int) -> Pagamento:
        pass

    def consultar_valor_restante(self):
        pass

    def validar_data_pagamento(self):
        pass
