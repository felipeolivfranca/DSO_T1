from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_profissional import ControladorProfissional
from entidade.atendimento import Atendimento
from entidade.procedimento import Procedimento
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from limite.tela_procedimento import TelaProcedimento


class ControladorProcedimento:
    def __init__(self, controlador_atendimento: ControladorAtendimento,
                 controlador_profissional: ControladorProfissional):
        self.__tela = TelaProcedimento()
        self.__proximo_id = 1
        self.__controlador_atendimento = controlador_atendimento
        self.__controlador_profissional = controlador_profissional

    def incluir_procedimento(self):
        atendimento = self.__controlador_atendimento.buscar_por_id(
            self.__tela.pega_id_atendimento())
        dados = self.__tela.pega_dados_procedimento()
        profissional = self.__controlador_profissional.buscar_por_cpf(dados["cpf_profissional"])
        procedimento = Procedimento(dados["descricao"], dados["custo"], profissional,
                                    self.__proximo_id)
        atendimento.adicionar_procedimento(procedimento)
        self.__proximo_id += 1
        self.__tela.mostra_mensagem(
            f"Procedimento {procedimento.id} registrado no atendimento {atendimento.id}!")

    def alterar_procedimento(self):
        procedimento = self.buscar_por_id(self.__tela.pega_id())
        dados = self.__tela.pega_dados_procedimento()
        profissional = self.__controlador_profissional.buscar_por_cpf(dados["cpf_profissional"])
        procedimento.descricao = dados["descricao"]
        procedimento.custo = dados["custo"]
        procedimento.profissional = profissional
        self.__tela.mostra_mensagem("Procedimento alterado com sucesso!")

    def excluir_procedimento(self):
        atendimento, procedimento = self.__buscar_com_atendimento(self.__tela.pega_id())
        atendimento.remover_procedimento(procedimento)
        self.__tela.mostra_mensagem("Procedimento excluído com sucesso!")

    def listar_procedimento(self):
        encontrou = False
        for atendimento in self.__controlador_atendimento.atendimentos:
            for procedimento in atendimento.procedimentos:
                encontrou = True
                self.__tela.mostra_procedimento({
                    "id": procedimento.id,
                    "id_atendimento": atendimento.id,
                    "descricao": procedimento.descricao,
                    "custo": procedimento.custo,
                    "profissional": procedimento.profissional.nome,
                })
        if not encontrou:
            self.__tela.mostra_mensagem("Nenhum procedimento registrado.")

    def abrir_tela(self):
        opcoes = {1: self.incluir_procedimento, 2: self.alterar_procedimento,
                  3: self.excluir_procedimento, 4: self.listar_procedimento}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_id(self, id: int) -> Procedimento:
        return self.__buscar_com_atendimento(id)[1]

    def __buscar_com_atendimento(self, id: int) -> tuple[Atendimento, Procedimento]:
        for atendimento in self.__controlador_atendimento.atendimentos:
            for procedimento in atendimento.procedimentos:
                if procedimento.id == id:
                    return atendimento, procedimento
        raise NaoEncontradoException(f"Procedimento {id} não encontrado")
