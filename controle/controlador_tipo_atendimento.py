from entidade.tipo_atendimento import TipoAtendimento
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from limite.tela_tipo_atendimento import TelaTipoAtendimento


class ControladorTipoAtendimento:
    def __init__(self):
        self.__tipos = [TipoAtendimento("Consulta"), TipoAtendimento("Exame"),
                        TipoAtendimento("Retorno")]
        self.__tela = TelaTipoAtendimento()

    def incluir_tipo_atendimento(self):
        dados = self.__tela.pega_dados_tipo()
        self.__valida_descricao_livre(dados["descricao"])
        self.__tipos.append(TipoAtendimento(dados["descricao"]))
        self.__tela.mostra_mensagem("Tipo de atendimento cadastrado com sucesso!")

    def alterar_tipo_atendimento(self):
        tipo = self.buscar_por_descricao(self.__tela.pega_descricao())
        dados = self.__tela.pega_dados_tipo()
        if dados["descricao"].lower() != tipo.descricao.lower():
            self.__valida_descricao_livre(dados["descricao"])
        tipo.descricao = dados["descricao"]
        self.__tela.mostra_mensagem("Tipo de atendimento alterado com sucesso!")

    def excluir_tipo_atendimento(self):
        tipo = self.buscar_por_descricao(self.__tela.pega_descricao())
        self.__tipos.remove(tipo)
        self.__tela.mostra_mensagem("Tipo de atendimento excluído com sucesso!")

    def listar_tipo_atendimento(self):
        if not self.__tipos:
            self.__tela.mostra_mensagem("Nenhum tipo de atendimento cadastrado.")
            return
        self.__tela.mostra_mensagem("\nTipos de atendimento:")
        for tipo in self.__tipos:
            self.__tela.mostra_tipo({"descricao": tipo.descricao})

    def abrir_tela(self):
        opcoes = {1: self.incluir_tipo_atendimento, 2: self.alterar_tipo_atendimento,
                  3: self.excluir_tipo_atendimento, 4: self.listar_tipo_atendimento}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_descricao(self, descricao: str) -> TipoAtendimento:
        for tipo in self.__tipos:
            if tipo.descricao.lower() == descricao.lower():
                return tipo
        raise NaoEncontradoException(f"Tipo de atendimento {descricao} não encontrado")

    def __valida_descricao_livre(self, descricao: str):
        if any(tipo.descricao.lower() == descricao.lower() for tipo in self.__tipos):
            raise JaCadastradoException(f"O tipo de atendimento {descricao} já existe")
