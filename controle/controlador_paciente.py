from datetime import date

from entidade.paciente import Paciente
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from limite.tela_paciente import TelaPaciente


class ControladorPaciente:
    def __init__(self):
        self.__pacientes = []
        self.__tela_paciente = TelaPaciente()

    def incluir_paciente(self):
        dados = self.__tela_paciente.pega_dados_paciente()
        self.__valida_cpf_livre(dados["cpf"])
        self.__pacientes.append(Paciente(dados["nome"], dados["celular"],
                                         dados["cpf"], dados["data_nascimento"]))
        self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso!")

    def alterar_paciente(self):
        paciente = self.buscar_por_cpf(self.__tela_paciente.pega_cpf())
        dados = self.__tela_paciente.pega_dados_paciente()
        if dados["cpf"] != paciente.cpf:
            self.__valida_cpf_livre(dados["cpf"])
        paciente.nome = dados["nome"]
        paciente.celular = dados["celular"]
        paciente.cpf = dados["cpf"]
        paciente.data_nascimento = dados["data_nascimento"]
        self.__tela_paciente.mostra_mensagem("Paciente alterado com sucesso!")

    def excluir_paciente(self):
        paciente = self.buscar_por_cpf(self.__tela_paciente.pega_cpf())
        self.__pacientes.remove(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente excluído com sucesso!")

    def buscar_por_cpf(self, cpf: str) -> Paciente:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        raise NaoEncontradoException(f"Paciente com CPF {cpf} não encontrado")

    def listar_paciente(self):
        if not self.__pacientes:
            self.__tela_paciente.mostra_mensagem("Nenhum paciente cadastrado.")
            return
        for paciente in self.__pacientes:
            self.__tela_paciente.mostra_paciente({
                "nome": paciente.nome,
                "celular": paciente.celular,
                "cpf": paciente.cpf,
                "data_nascimento": paciente.data_nascimento,
                "idade": paciente.calcularIdade(date.today()),
            })

    def abrir_tela(self):
        opcoes = {1: self.incluir_paciente, 2: self.alterar_paciente,
                  3: self.excluir_paciente, 4: self.listar_paciente}
        while True:
            opcao = self.__tela_paciente.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException) as e:
                self.__tela_paciente.mostra_mensagem(f"Erro: {e}")

    def __valida_cpf_livre(self, cpf: str):
        if any(paciente.cpf == cpf for paciente in self.__pacientes):
            raise JaCadastradoException(f"Já existe um paciente com o CPF {cpf}")
