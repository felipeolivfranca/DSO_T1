from entidade.profissional_saude import ProfissionalSaude
from limite.tela_profissional import TelaProfissional


class ControladorProfissional:
    def __init__(self):
        self.__profissionais = []
        self.__tela = TelaProfissional()

    def incluir_profissional(self):
        pass

    def alterar_profissional(self):
        pass

    def excluir_profissional(self):
        pass

    def listar_profissional(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_cpf(self, cpf: str) -> ProfissionalSaude:
        pass
