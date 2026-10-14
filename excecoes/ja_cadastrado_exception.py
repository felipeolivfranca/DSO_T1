class JaCadastradoException(Exception):
    def __init__(self, mensagem: str = "Registro já cadastrado"):
        super().__init__(mensagem)
