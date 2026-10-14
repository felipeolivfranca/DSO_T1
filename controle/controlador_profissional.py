from entidade.profissional_saude import ProfissionalSaude
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from limite.tela_profissional import TelaProfissional


class ControladorProfissional:
    def __init__(self):
        self.__profissionais = []
        self.__tela = TelaProfissional()

    def incluir_profissional(self):
        dados = self.__tela.pega_dados_profissional()
        self.__valida_dados_livres(dados["cpf"], dados["registro_profissional"])
        self.__profissionais.append(ProfissionalSaude(
            dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"],
            dados["especialidade"], dados["registro_profissional"]))
        self.__tela.mostra_mensagem("Profissional cadastrado com sucesso!")

    def alterar_profissional(self):
        profissional = self.buscar_por_cpf(self.__tela.pega_cpf())
        dados = self.__tela.pega_dados_profissional()
        self.__valida_dados_livres(dados["cpf"], dados["registro_profissional"], profissional)
        profissional.nome = dados["nome"]
        profissional.celular = dados["celular"]
        profissional.cpf = dados["cpf"]
        profissional.data_nascimento = dados["data_nascimento"]
        profissional.especialidade = dados["especialidade"]
        profissional.registro_profissional = dados["registro_profissional"]
        self.__tela.mostra_mensagem("Profissional alterado com sucesso!")

    def excluir_profissional(self):
        profissional = self.buscar_por_cpf(self.__tela.pega_cpf())
        self.__profissionais.remove(profissional)
        self.__tela.mostra_mensagem("Profissional excluído com sucesso!")

    def listar_profissional(self):
        if not self.__profissionais:
            self.__tela.mostra_mensagem("Nenhum profissional cadastrado.")
            return
        for profissional in self.__profissionais:
            self.__tela.mostra_profissional({
                "nome": profissional.nome,
                "celular": profissional.celular,
                "cpf": profissional.cpf,
                "data_nascimento": profissional.data_nascimento,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
            })

    def abrir_tela(self):
        opcoes = {1: self.incluir_profissional, 2: self.alterar_profissional,
                  3: self.excluir_profissional, 4: self.listar_profissional}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (JaCadastradoException, NaoEncontradoException) as e:
                self.__tela.mostra_mensagem(f"Erro: {e}")

    def buscar_por_cpf(self, cpf: str) -> ProfissionalSaude:
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        raise NaoEncontradoException(f"Profissional com CPF {cpf} não encontrado")

    def __valida_dados_livres(self, cpf: str, registro: str,
                              ignorar: ProfissionalSaude = None):
        for profissional in self.__profissionais:
            if profissional is ignorar:
                continue
            if profissional.cpf == cpf:
                raise JaCadastradoException(f"Já existe um profissional com o CPF {cpf}")
            if profissional.registro_profissional.lower() == registro.lower():
                raise JaCadastradoException(
                    f"Já existe um profissional com o registro {registro}")
