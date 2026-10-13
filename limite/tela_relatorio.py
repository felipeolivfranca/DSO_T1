from limite.tela import Tela


class TelaRelatorio(Tela):
    def mostra_menu(self) -> int:
        pass

    def mostra_ranking_clinicas(self, ranking: list):
        pass

    def mostra_extremos_atendimentos(self, maior: dict, menor: dict):
        pass

    def mostra_ranking_procedimentos(self, ranking: list):
        pass

    def mostra_extremos_procedimentos(self, maior: dict, menor: dict):
        pass
