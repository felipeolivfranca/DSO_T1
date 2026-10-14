from datetime import date, time
from decimal import Decimal

from entidade.clinica import Clinica
from entidade.paciente import Paciente
from entidade.pagamento import Pagamento
from entidade.pessoa import Pessoa
from entidade.procedimento import Procedimento
from entidade.profissional_saude import ProfissionalSaude
from entidade.tipo_atendimento import TipoAtendimento
from excecoes.ja_cadastrado_exception import JaCadastradoException
from excecoes.nao_encontrado_exception import NaoEncontradoException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException


class Atendimento:
    def __init__(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude,
                 data_atendimento: date, horario_inicio: time, horario_fim: time,
                 tipo_atendimento: TipoAtendimento, valor: Decimal, id_atendimento: int):
        self.__id = id_atendimento
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__responsavel = None
        self.__data = data_atendimento
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo = tipo_atendimento
        self.__valor = valor
        self.__pagamentos = []
        self.__procedimentos = []

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = profissional

    @property
    def responsavel(self) -> Pessoa:
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel: Pessoa):
        self.__responsavel = responsavel

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def horario_inicio(self) -> time:
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: time):
        self.__horario_inicio = horario_inicio

    @property
    def horario_fim(self) -> time:
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, horario_fim: time):
        self.__horario_fim = horario_fim

    @property
    def tipo(self) -> TipoAtendimento:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoAtendimento):
        self.__tipo = tipo

    @property
    def valor(self) -> Decimal:
        return self.__valor

    @valor.setter
    def valor(self, valor: Decimal):
        self.__valor = valor

    @property
    def pagamentos(self) -> list[Pagamento]:
        return self.__pagamentos

    @property
    def procedimentos(self) -> list[Procedimento]:
        return self.__procedimentos

    def adicionarProcedimento(self, p: Procedimento):
        if any(proc.id == p.id for proc in self.__procedimentos):
            raise JaCadastradoException(
                f"Procedimento {p.id} já registrado no atendimento {self.__id}")
        self.__procedimentos.append(p)

    def removerProcedimento(self, p: Procedimento):
        for proc in self.__procedimentos:
            if proc.id == p.id:
                self.__procedimentos.remove(proc)
                return
        raise NaoEncontradoException(
            f"Procedimento {p.id} não pertence ao atendimento {self.__id}")

    def adicionarPagamento(self, pg: Pagamento):
        if any(pag.id == pg.id for pag in self.__pagamentos):
            raise JaCadastradoException(
                f"Pagamento {pg.id} já registrado no atendimento {self.__id}")
        if pg.data > self.__data:
            raise PagamentoInvalidoException(
                "O pagamento deve ser realizado até a data do atendimento")
        if pg.valor_pago <= 0:
            raise PagamentoInvalidoException("O valor pago deve ser maior que zero")
        if pg.valor_pago > self.calcularTotalRestante():
            raise PagamentoInvalidoException(
                f"O valor pago excede o restante ({self.calcularTotalRestante()})")
        self.__pagamentos.append(pg)

    def calcularValorTotal(self) -> Decimal:
        return self.__valor + sum((proc.custo for proc in self.__procedimentos), Decimal(0))

    def calcularTotalPago(self) -> Decimal:
        return sum((pag.valor_pago for pag in self.__pagamentos), Decimal(0))

    def calcularTotalRestante(self) -> Decimal:
        return self.calcularValorTotal() - self.calcularTotalPago()

    def estaQuitado(self) -> bool:
        return self.calcularTotalRestante() <= 0

    def pacienteEhMenor(self) -> bool:
        return not self.__paciente.ehMaiorDeIdade(self.__data)
