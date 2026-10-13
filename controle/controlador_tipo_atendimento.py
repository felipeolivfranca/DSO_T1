from entidade.tipo_atendimento import TipoAtendimento
from limite.tela_tipo_atendimento import TelaTipoAtendimento


class ControladorTipoAtendimento:
    def __init__(self):
        self.__tipos = []
        self.__tela = TelaTipoAtendimento()

    def incluir_tipo_atendimento(self):
        pass

    def alterar_tipo_atendimento(self):
        pass

    def excluir_tipo_atendimento(self):
        pass

    def listar_tipo_atendimento(self):
        pass

    def abrir_tela(self):
        pass

    def buscar_por_descricao(self, descricao: str) -> TipoAtendimento:
        pass
