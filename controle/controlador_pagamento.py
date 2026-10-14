from datetime import date

from controle.controlador_atendimento import ControladorAtendimento
from entidade.atendimento import Atendimento
from entidade.pagamento import Pagamento
from entidade.pagamento_cartao_credito import PagamentoCartaoCredito
from entidade.pagamento_dinheiro import PagamentoDinheiro
from entidade.pagamento_pix import PagamentoPix
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException
from limite.tela_pagamento import TelaPagamento


class ControladorPagamento:
    def __init__(self, controlador_atendimento: ControladorAtendimento):
        self.__pagamentos = []
        self.__tela = TelaPagamento()
        self.__proximo_id = 1
        self.__controlador_atendimento = controlador_atendimento

    def incluir_pagamento(self):
        forma = self.__tela.pega_forma()
        dados = self.__tela.pega_dados_pagamento()
        atendimento = self.__controlador_atendimento.buscar_por_id(dados["id_atendimento"])
        self.validar_data_pagamento(dados["data"], atendimento)
        argumentos = (self.__proximo_id, dados["data"], atendimento, atendimento.paciente,
                      dados["valor_pago"])
        if forma == TelaPagamento.PIX:
            pagamento = PagamentoPix(*argumentos, self.__tela.pega_dados_pix()["cpf_pagador"])
        elif forma == TelaPagamento.CARTAO:
            cartao = self.__tela.pega_dados_cartao()
            pagamento = PagamentoCartaoCredito(*argumentos, cartao["numero_cartao"],
                                               cartao["bandeira"])
        else:
            pagamento = PagamentoDinheiro(*argumentos)
        atendimento.adicionarPagamento(pagamento)
        self.__pagamentos.append(pagamento)
        self.__proximo_id += 1
        self.__tela.mostra_mensagem(f"Pagamento {pagamento.id} registrado com sucesso!")
        self.__tela.mostra_valor_restante(pagamento.calcular_valor_restante())

    def alterar_pagamento(self):
        pagamento = self.buscar_por_id(self.__tela.pega_id())
        dados = self.__tela.pega_dados_pagamento(com_atendimento=False)
        atendimento = pagamento.atendimento
        self.validar_data_pagamento(dados["data"], atendimento)
        disponivel = atendimento.calcularTotalRestante() + pagamento.valor_pago
        if dados["valor_pago"] <= 0:
            raise PagamentoInvalidoException("O valor pago deve ser maior que zero")
        if dados["valor_pago"] > disponivel:
            raise PagamentoInvalidoException(f"O valor pago excede o restante ({disponivel})")
        if isinstance(pagamento, PagamentoPix):
            pagamento.cpf_pagador = self.__tela.pega_dados_pix()["cpf_pagador"]
        elif isinstance(pagamento, PagamentoCartaoCredito):
            cartao = self.__tela.pega_dados_cartao()
            pagamento.numero_cartao = cartao["numero_cartao"]
            pagamento.bandeira = cartao["bandeira"]
        pagamento.data = dados["data"]
        pagamento.valor_pago = dados["valor_pago"]
        self.__tela.mostra_mensagem("Pagamento alterado com sucesso!")
        self.__tela.mostra_valor_restante(pagamento.calcular_valor_restante())

    def excluir_pagamento(self):
        pagamento = self.buscar_por_id(self.__tela.pega_id())
        pagamento.atendimento.removerPagamento(pagamento)
        self.__pagamentos.remove(pagamento)
        self.__tela.mostra_mensagem("Pagamento excluído com sucesso!")

    def listar_pagamento(self):
        if not self.__pagamentos:
            self.__tela.mostra_mensagem("Nenhum pagamento registrado.")
            return
        for pagamento in self.__pagamentos:
            self.__tela.mostra_pagamento({
                "id": pagamento.id,
                "forma": pagamento.descrever_forma(),
                "id_atendimento": pagamento.atendimento.id,
                "paciente": pagamento.paciente.nome,
                "data": pagamento.data,
                "valor_pago": pagamento.valor_pago,
                "restante": pagamento.calcular_valor_restante(),
            })

    def abrir_tela(self):
        opcoes = {1: self.incluir_pagamento, 2: self.alterar_pagamento,
                  3: self.excluir_pagamento, 4: self.listar_pagamento,
                  5: self.consultar_valor_restante}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException,
                    PagamentoInvalidoException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_id(self, id: int) -> Pagamento:
        for pagamento in self.__pagamentos:
            if pagamento.id == id:
                return pagamento
        raise NaoEncontradoException(f"Pagamento {id} não encontrado")

    def consultar_valor_restante(self):
        atendimento = self.__controlador_atendimento.buscar_por_id(
            self.__tela.pega_id("ID do atendimento: "))
        self.__tela.mostra_valor_restante(atendimento.calcularTotalRestante())

    def validar_data_pagamento(self, data: date, atendimento: Atendimento):
        if data > atendimento.data:
            raise PagamentoInvalidoException(
                "O pagamento deve ser realizado até a data do atendimento "
                f"({atendimento.data.strftime('%d/%m/%Y')})")
