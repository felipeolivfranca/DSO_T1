from abc import ABC, abstractmethod
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation


class Tela(ABC):
    def le_num_inteiro(self, mensagem: str, validos: list = None) -> int:
        while True:
            try:
                valor = int(input(mensagem))
                if validos and valor not in validos:
                    raise ValueError
                return valor
            except ValueError:
                print("Valor incorreto! Digite um número inteiro válido.")
                if validos:
                    print("Valores válidos:", ", ".join(str(v) for v in validos))

    def le_texto(self, mensagem: str) -> str:
        while True:
            texto = input(mensagem).strip()
            if texto:
                return texto
            print("O campo não pode ficar vazio.")

    def le_valor_decimal(self, mensagem: str) -> Decimal:
        while True:
            try:
                valor = Decimal(input(mensagem).strip().replace(",", "."))
                if not valor.is_finite() or valor < 0:
                    raise ValueError
                return valor
            except (InvalidOperation, ValueError):
                print("Valor incorreto! Digite um número maior ou igual a zero (ex.: 150,00).")

    def le_data(self, mensagem: str) -> date:
        while True:
            try:
                return datetime.strptime(input(mensagem).strip(), "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida! Use o formato dd/mm/aaaa.")

    def le_hora(self, mensagem: str) -> time:
        while True:
            try:
                return datetime.strptime(input(mensagem).strip(), "%H:%M").time()
            except ValueError:
                print("Horário inválido! Use o formato hh:mm.")

    def le_cpf(self, mensagem: str) -> str:
        while True:
            cpf = input(mensagem).strip().replace(".", "").replace("-", "")
            if cpf.isdigit() and len(cpf) == 11:
                return cpf
            print("CPF inválido! Digite os 11 números do CPF.")

    def mostra_mensagem(self, mensagem: str):
        print(mensagem)

    def formata_data(self, data: date) -> str:
        return data.strftime("%d/%m/%Y")

    def formata_hora(self, horario: time) -> str:
        return horario.strftime("%H:%M")

    def formata_valor(self, valor: Decimal) -> str:
        return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @abstractmethod
    def mostra_menu(self) -> int:
        pass
