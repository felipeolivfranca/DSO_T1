"""Preenche o sistema com dados de exemplo para testes manuais.

Uso: py main.py --exemplo

Os dados são "digitados" automaticamente pelos menus do próprio sistema, então
passam pelas mesmas validações que uma pessoa usando o programa. Quando acabam,
o controle volta para o teclado no menu principal.
"""
import builtins
import io
import sys

PACIENTES = [
    # nome, celular, CPF, nascimento
    ("João Silva", "48991110001", "11111111111", "15/03/1985"),
    ("Maria Souza", "48991110002", "22222222222", "08/07/1992"),
    ("Pedro Santos", "48991110003", "33333333333", "30/11/1978"),
    ("Bia Lima", "48991110004", "44444444444", "21/10/2012"),       # menor de idade
    ("Lucas Costa", "48991110005", "55555555555", "05/05/2015"),    # menor de idade
]

PROFISSIONAIS = [
    # nome, celular, CPF, nascimento, especialidade, registro
    ("Ana Ribeiro", "48992220001", "66666666666", "12/04/1980", "Cardiologia", "CRM-SC 1001"),
    ("Carlos Mendes", "48992220002", "77777777777", "23/09/1975", "Ortopedia", "CRM-SC 1002"),
    ("Fernanda Alves", "48992220003", "88888888888", "02/02/1988", "Pediatria", "CRM-SC 1003"),
]

CLINICAS = [
    # nome, cidade, descrição, abertura, fechamento
    ("Vida", "Florianópolis", "Clínica geral", "08:00", "18:00"),
    ("Saúde Total", "São José", "Exames e ortopedia", "07:00", "19:00"),
    ("Plantão 24h", "Palhoça", "Pronto atendimento", "00:00", "00:00"),
]

VINCULOS = [
    # clínica, CPF do profissional
    ("Vida", "66666666666"), ("Vida", "88888888888"),
    ("Saúde Total", "77777777777"), ("Saúde Total", "66666666666"),
    ("Plantão 24h", "77777777777"), ("Plantão 24h", "88888888888"),
]

TIPOS_EXTRAS = ["Teleconsulta"]

ATENDIMENTOS = [
    # clínica, CPF paciente, CPF profissional, data, início, fim, tipo, valor, CPF responsável
    ("Vida", "11111111111", "66666666666", "10/11/2026", "09:00", "10:00", "Consulta", "250", None),
    ("Vida", "44444444444", "88888888888", "10/11/2026", "10:00", "10:30", "Consulta", "180",
     "22222222222"),
    ("Saúde Total", "33333333333", "77777777777", "11/11/2026", "14:00", "15:00", "Exame", "400",
     None),
    ("Saúde Total", "22222222222", "66666666666", "12/11/2026", "08:00", "09:00", "Retorno",
     "120", None),
    ("Plantão 24h", "55555555555", "88888888888", "12/11/2026", "23:30", "00:30", "Consulta",
     "300", "33333333333"),
    ("Plantão 24h", "11111111111", "77777777777", "13/11/2026", "02:00", "03:00", "Exame", "350",
     None),
    ("Vida", "22222222222", "66666666666", "14/11/2026", "15:00", "16:00", "Teleconsulta", "150",
     None),
]

PROCEDIMENTOS = [
    # ID do atendimento, descrição, custo, CPF do profissional
    (1, "Eletrocardiograma", "120", "66666666666"),
    (2, "Vacina", "80", "88888888888"),
    (3, "Raio-X", "180", "77777777777"),
    (3, "Imobilização", "90", "77777777777"),
    (4, "Eletrocardiograma", "120", "66666666666"),
    (5, "Nebulização", "60", "88888888888"),
    (6, "Raio-X", "180", "77777777777"),
]

PAGAMENTOS = [
    # forma (1 dinheiro, 2 PIX, 3 cartão), ID do atendimento, data, valor, dados da forma
    ("2", 1, "05/11/2026", "200", ["11111111111"]),
    ("1", 1, "10/11/2026", "170", []),
    ("1", 2, "10/11/2026", "260", []),
    ("3", 3, "11/11/2026", "300", ["4111111111111111", "Visa"]),
    ("2", 6, "01/11/2026", "100", ["11111111111"]),
]


def montar_entradas() -> list[str]:
    """Sequência de respostas aos menus que cadastra todos os dados acima."""
    entradas = ["1"]
    for paciente in PACIENTES:
        entradas += ["1", *paciente]
    entradas += ["0", "2"]
    for profissional in PROFISSIONAIS:
        entradas += ["1", *profissional]
    entradas += ["0", "3"]
    for clinica in CLINICAS:
        entradas += ["1", *clinica]
    for clinica, cpf in VINCULOS:
        entradas += ["5", clinica, cpf]
    entradas += ["0", "4"]
    for tipo in TIPOS_EXTRAS:
        entradas += ["1", tipo]
    entradas += ["0", "5"]
    for *dados, responsavel in ATENDIMENTOS:
        entradas += ["1", *dados] + ([responsavel] if responsavel else [])
    entradas += ["0", "6"]
    for id_atendimento, *dados in PROCEDIMENTOS:
        entradas += ["1", str(id_atendimento), *dados]
    entradas += ["0", "7"]
    for forma, id_atendimento, data, valor, extras in PAGAMENTOS:
        entradas += ["1", forma, str(id_atendimento), data, valor, *extras]
    entradas += ["0"]
    return entradas


def ativar():
    """Faz as próximas chamadas de input() responderem com os dados de exemplo.

    Enquanto os dados são carregados, a saída fica escondida. Ao terminar, mostra
    um resumo, reexibe o menu principal e volta a ler do teclado.
    """
    fila = montar_entradas()
    input_original = builtins.input
    saida_original = sys.stdout
    saida_oculta = io.StringIO()
    inicio_ultimo_trecho = 0
    sys.stdout = saida_oculta

    def input_com_dados(prompt=""):
        nonlocal inicio_ultimo_trecho
        if fila:
            inicio_ultimo_trecho = saida_oculta.tell()
            return fila.pop(0)

        builtins.input = input_original
        sys.stdout = saida_original
        texto = saida_oculta.getvalue()
        erros = [linha for linha in texto.splitlines() if "Erro" in linha]
        print(f"Dados de exemplo carregados: {len(PACIENTES)} pacientes, "
              f"{len(PROFISSIONAIS)} profissionais, {len(CLINICAS)} clínicas, "
              f"{len(ATENDIMENTOS)} atendimentos, {len(PROCEDIMENTOS)} procedimentos e "
              f"{len(PAGAMENTOS)} pagamentos.")
        for erro in erros:
            print(f"Atenção, falha ao carregar: {erro}")
        print(texto[inicio_ultimo_trecho:], end="")
        return input_original(prompt)

    builtins.input = input_com_dados
