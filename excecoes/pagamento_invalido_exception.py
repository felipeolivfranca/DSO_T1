class PagamentoInvalidoException(Exception):
    def __init__(self, mensagem: str = "Pagamento inválido"):
        super().__init__(mensagem)
