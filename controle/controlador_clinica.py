from controle.controlador_profissional import ControladorProfissional
from entidade.clinica import Clinica
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.operacao_invalida_exception import OperacaoInvalidaException
from limite.tela_clinica import TelaClinica


class ControladorClinica:
    def __init__(self, controlador_profissional: ControladorProfissional):
        self.__clinicas = []
        self.__tela = TelaClinica()
        self.__controlador_profissional = controlador_profissional

    @property
    def clinicas(self) -> list[Clinica]:
        return self.__clinicas

    def incluir_clinica(self):
        dados = self.__tela.pega_dados_clinica()
        self.__valida_nome_livre(dados["nome"])
        self.__clinicas.append(Clinica(dados["nome"], dados["cidade"], dados["descricao"],
                                       dados["horario_abertura"], dados["horario_fechamento"]))
        self.__tela.mostra_mensagem("Clínica cadastrada com sucesso!")

    def alterar_clinica(self):
        clinica = self.buscar_por_nome(self.__tela.pega_nome())
        dados = self.__tela.pega_dados_clinica()
        if dados["nome"].lower() != clinica.nome.lower():
            self.__valida_nome_livre(dados["nome"])
        clinica.nome = dados["nome"]
        clinica.cidade = dados["cidade"]
        clinica.descricao = dados["descricao"]
        clinica.horario_abertura = dados["horario_abertura"]
        clinica.horario_fechamento = dados["horario_fechamento"]
        self.__tela.mostra_mensagem("Clínica alterada com sucesso!")

    def excluir_clinica(self):
        clinica = self.buscar_por_nome(self.__tela.pega_nome())
        if clinica.total_atendimentos() > 0:
            raise OperacaoInvalidaException(
                f"A clínica {clinica.nome} possui atendimentos e não pode ser excluída")
        self.__clinicas.remove(clinica)
        self.__tela.mostra_mensagem("Clínica excluída com sucesso!")

    def listar_clinica(self):
        if not self.__clinicas:
            self.__tela.mostra_mensagem("Nenhuma clínica cadastrada.")
            return
        for clinica in self.__clinicas:
            self.__tela.mostra_clinica({
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "descricao": clinica.descricao,
                "horario_abertura": clinica.horario_abertura,
                "horario_fechamento": clinica.horario_fechamento,
                "profissionais": [p.nome for p in clinica.profissionais],
                "total_atendimentos": clinica.total_atendimentos(),
            })

    def abrir_tela(self):
        opcoes = {1: self.incluir_clinica, 2: self.alterar_clinica,
                  3: self.excluir_clinica, 4: self.listar_clinica,
                  5: self.vincular_profissional, 6: self.desvincular_profissional}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException,
                    OperacaoInvalidaException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_nome(self, nome: str) -> Clinica:
        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome.lower():
                return clinica
        raise NaoEncontradoException(f"Clínica {nome} não encontrada")

    def vincular_profissional(self):
        clinica = self.buscar_por_nome(self.__tela.pega_nome())
        profissional = self.__controlador_profissional.buscar_por_cpf(
            self.__tela.pega_cpf_profissional())
        clinica.adicionar_profissional(profissional)
        self.__tela.mostra_mensagem(f"{profissional.nome} vinculado à clínica {clinica.nome}!")

    def desvincular_profissional(self):
        clinica = self.buscar_por_nome(self.__tela.pega_nome())
        profissional = self.__controlador_profissional.buscar_por_cpf(
            self.__tela.pega_cpf_profissional())
        clinica.remover_profissional(profissional)
        self.__tela.mostra_mensagem(
            f"{profissional.nome} desvinculado da clínica {clinica.nome}!")

    def __valida_nome_livre(self, nome: str):
        if any(clinica.nome.lower() == nome.lower() for clinica in self.__clinicas):
            raise JaCadastradoException(f"Já existe uma clínica com o nome {nome}")
