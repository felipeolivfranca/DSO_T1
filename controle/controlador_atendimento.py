from datetime import date, time

from controle.controlador_clinica import ControladorClinica
from controle.controlador_paciente import ControladorPaciente
from controle.controlador_profissional import ControladorProfissional
from controle.controlador_tipo_atendimento import ControladorTipoAtendimento
from entidade.atendimento import Atendimento
from entidade.clinica import Clinica
from entidade.paciente import Paciente
from entidade.pessoa import Pessoa
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.operacao_invalida_exception import OperacaoInvalidaException
from limite.tela_atendimento import TelaAtendimento


class ControladorAtendimento:
    def __init__(self, controlador_paciente: ControladorPaciente,
                 controlador_profissional: ControladorProfissional,
                 controlador_tipo_atendimento: ControladorTipoAtendimento,
                 controlador_clinica: ControladorClinica):
        self.__atendimentos = []
        self.__tela = TelaAtendimento()
        self.__proximo_id = 1
        self.__controlador_paciente = controlador_paciente
        self.__controlador_profissional = controlador_profissional
        self.__controlador_tipo_atendimento = controlador_tipo_atendimento
        self.__controlador_clinica = controlador_clinica

    @property
    def atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    def incluir_atendimento(self):
        dados = self.__pega_dados_validados()
        atendimento = Atendimento(dados["clinica"], dados["paciente"], dados["profissional"],
                                  dados["data"], dados["horario_inicio"], dados["horario_fim"],
                                  dados["tipo"], dados["valor"], self.__proximo_id)
        atendimento.responsavel = dados["responsavel"]
        dados["clinica"].adicionar_atendimento(atendimento)
        self.__atendimentos.append(atendimento)
        self.__proximo_id += 1
        self.__tela.mostra_mensagem(f"Atendimento {atendimento.id} cadastrado com sucesso!")

    def alterar_atendimento(self):
        atendimento = self.buscar_por_id(self.__tela.pega_id())
        dados = self.__pega_dados_validados()
        if any(pagamento.data > dados["data"] for pagamento in atendimento.pagamentos):
            raise OperacaoInvalidaException(
                "Já existem pagamentos posteriores à nova data do atendimento")
        if dados["clinica"] is not atendimento.clinica:
            atendimento.clinica.remover_atendimento(atendimento)
            dados["clinica"].adicionar_atendimento(atendimento)
        atendimento.clinica = dados["clinica"]
        atendimento.paciente = dados["paciente"]
        atendimento.responsavel = dados["responsavel"]
        atendimento.profissional = dados["profissional"]
        atendimento.data = dados["data"]
        atendimento.horario_inicio = dados["horario_inicio"]
        atendimento.horario_fim = dados["horario_fim"]
        atendimento.tipo = dados["tipo"]
        atendimento.valor = dados["valor"]
        self.__tela.mostra_mensagem("Atendimento alterado com sucesso!")

    def excluir_atendimento(self):
        atendimento = self.buscar_por_id(self.__tela.pega_id())
        if atendimento.pagamentos:
            raise OperacaoInvalidaException(
                "O atendimento possui pagamentos; exclua os pagamentos antes")
        atendimento.clinica.remover_atendimento(atendimento)
        self.__atendimentos.remove(atendimento)
        self.__tela.mostra_mensagem("Atendimento excluído com sucesso!")

    def listar_atendimento(self):
        if not self.__atendimentos:
            self.__tela.mostra_mensagem("Nenhum atendimento cadastrado.")
            return
        for atendimento in self.__atendimentos:
            self.__tela.mostra_atendimento({
                "id": atendimento.id,
                "clinica": atendimento.clinica.nome,
                "paciente": atendimento.paciente.nome,
                "responsavel": atendimento.responsavel.nome if atendimento.responsavel else None,
                "profissional": atendimento.profissional.nome,
                "data": atendimento.data,
                "horario_inicio": atendimento.horario_inicio,
                "horario_fim": atendimento.horario_fim,
                "tipo": atendimento.tipo.descricao,
                "valor": atendimento.valor,
                "valor_total": atendimento.calcular_valor_total(),
                "total_pago": atendimento.calcular_total_pago(),
                "restante": atendimento.calcular_total_restante(),
                "quitado": atendimento.esta_quitado(),
                "procedimentos": [p.descricao for p in atendimento.procedimentos],
            })

    def abrir_tela(self):
        opcoes = {1: self.incluir_atendimento, 2: self.alterar_atendimento,
                  3: self.excluir_atendimento, 4: self.listar_atendimento}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException,
                    OperacaoInvalidaException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_id(self, id: int) -> Atendimento:
        for atendimento in self.__atendimentos:
            if atendimento.id == id:
                return atendimento
        raise NaoEncontradoException(f"Atendimento {id} não encontrado")

    def __pega_dados_validados(self) -> dict:
        dados = self.__tela.pega_dados_atendimento()
        dados["clinica"] = self.__controlador_clinica.buscar_por_nome(dados["clinica"])
        dados["paciente"] = self.__controlador_paciente.buscar_por_cpf(dados["cpf_paciente"])
        dados["profissional"] = self.__controlador_profissional.buscar_por_cpf(
            dados["cpf_profissional"])
        dados["tipo"] = self.__controlador_tipo_atendimento.buscar_por_descricao(dados["tipo"])

        if dados["profissional"] not in dados["clinica"].profissionais:
            raise OperacaoInvalidaException(
                f"{dados['profissional'].nome} não está vinculado à clínica "
                f"{dados['clinica'].nome}")
        self.__validar_horario_clinica(dados["clinica"], dados["horario_inicio"],
                                       dados["horario_fim"])

        dados["responsavel"] = None
        if not dados["paciente"].eh_maior_de_idade(dados["data"]):
            self.__tela.mostra_mensagem(
                "Paciente menor de idade: é obrigatório informar um responsável.")
            dados["responsavel"] = self.__buscar_pessoa(self.__tela.pega_cpf_atendimento())
        self.__validar_idade_e_responsavel(dados["paciente"], dados["responsavel"],
                                           dados["data"])
        return dados

    def __buscar_pessoa(self, cpf: str) -> Pessoa:
        try:
            return self.__controlador_paciente.buscar_por_cpf(cpf)
        except NaoEncontradoException:
            pass
        try:
            return self.__controlador_profissional.buscar_por_cpf(cpf)
        except NaoEncontradoException:
            raise NaoEncontradoException(f"Nenhuma pessoa cadastrada com o CPF {cpf}")

    def __validar_idade_e_responsavel(self, paciente: Paciente, responsavel: Pessoa,
                                      data_atendimento: date):
        if paciente.eh_maior_de_idade(data_atendimento):
            return
        if responsavel is None:
            raise OperacaoInvalidaException(
                "Pacientes menores de 18 anos precisam de um responsável")
        if responsavel.cpf == paciente.cpf:
            raise OperacaoInvalidaException("O paciente não pode ser o próprio responsável")
        if not responsavel.eh_maior_de_idade(data_atendimento):
            raise OperacaoInvalidaException("O responsável deve ter 18 anos ou mais")

    def __validar_horario_clinica(self, clinica: Clinica, inicio: time, fim: time):
        if inicio == fim:
            raise OperacaoInvalidaException("O horário de início e de fim não podem ser iguais")
        if not clinica.funciona_no_horario(inicio, fim):
            raise OperacaoInvalidaException(
                f"O atendimento deve ocorrer dentro do horário de funcionamento da clínica "
                f"({clinica.horario_abertura.strftime('%H:%M')} às "
                f"{clinica.horario_fechamento.strftime('%H:%M')})")
