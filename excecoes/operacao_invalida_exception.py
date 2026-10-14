class OperacaoInvalidaException(Exception):
    def __init__(self, mensagem: str = "Operação inválida"):
        super().__init__(mensagem)
