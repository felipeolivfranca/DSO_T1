from controle.controlador_atendimento import ControladorAtendimento
from controle.controlador_clinica import ControladorClinica
from excecoes.nao_encontrado_exception import NaoEncontradoException
from limite.tela_relatorio import TelaRelatorio


class ControladorRelatorio:
    def __init__(self, controlador_clinica: ControladorClinica,
                 controlador_atendimento: ControladorAtendimento):
        self.__tela = TelaRelatorio()
        self.__controlador_clinica = controlador_clinica
        self.__controlador_atendimento = controlador_atendimento

    def clinicas_com_mais_atendimentos(self):
        clinicas = self.__controlador_clinica.clinicas
        if not clinicas:
            raise NaoEncontradoException("Nenhuma clínica cadastrada")
        ordenadas = sorted(clinicas, key=lambda c: c.total_atendimentos(), reverse=True)
        self.__tela.mostra_ranking_clinicas([
            {"nome": c.nome, "cidade": c.cidade, "total": c.total_atendimentos()}
            for c in ordenadas
        ])

    def atendimentos_mais_caros_e_baratos(self):
        atendimentos = self.__controlador_atendimento.atendimentos
        if not atendimentos:
            raise NaoEncontradoException("Nenhum atendimento cadastrado")
        maior = max(atendimentos, key=lambda a: a.calcular_valor_total())
        menor = min(atendimentos, key=lambda a: a.calcular_valor_total())
        self.__tela.mostra_extremos_atendimentos(self.__dados_atendimento(maior),
                                                 self.__dados_atendimento(menor))

    def procedimentos_mais_realizados(self):
        contagem = {}
        for _, procedimento in self.__todos_procedimentos():
            chave = procedimento.descricao.strip().lower()
            if chave not in contagem:
                contagem[chave] = {"descricao": procedimento.descricao, "quantidade": 0}
            contagem[chave]["quantidade"] += 1
        ranking = sorted(contagem.values(), key=lambda item: item["quantidade"], reverse=True)
        self.__tela.mostra_ranking_procedimentos(ranking)

    def procedimentos_mais_caros_e_baratos(self):
        procedimentos = self.__todos_procedimentos()
        maior = max(procedimentos, key=lambda par: par[1].custo)
        menor = min(procedimentos, key=lambda par: par[1].custo)
        self.__tela.mostra_extremos_procedimentos(self.__dados_procedimento(*maior),
                                                  self.__dados_procedimento(*menor))

    def abrir_tela(self):
        opcoes = {1: self.clinicas_com_mais_atendimentos,
                  2: self.atendimentos_mais_caros_e_baratos,
                  3: self.procedimentos_mais_realizados,
                  4: self.procedimentos_mais_caros_e_baratos}
        while True:
            opcao = self.__tela.mostra_menu()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except NaoEncontradoException as e:
                self.__tela.mostra_mensagem(f"Não há dados para o relatório: {e}")

    def __todos_procedimentos(self) -> list:
        procedimentos = [(atendimento, procedimento)
                         for atendimento in self.__controlador_atendimento.atendimentos
                         for procedimento in atendimento.procedimentos]
        if not procedimentos:
            raise NaoEncontradoException("Nenhum procedimento registrado")
        return procedimentos

    def __dados_atendimento(self, atendimento) -> dict:
        return {
            "id": atendimento.id,
            "paciente": atendimento.paciente.nome,
            "clinica": atendimento.clinica.nome,
            "data": atendimento.data,
            "valor_total": atendimento.calcular_valor_total(),
        }

    def __dados_procedimento(self, atendimento, procedimento) -> dict:
        return {
            "id": procedimento.id,
            "id_atendimento": atendimento.id,
            "descricao": procedimento.descricao,
            "profissional": procedimento.profissional.nome,
            "custo": procedimento.custo,
        }
