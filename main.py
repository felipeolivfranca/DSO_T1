import sys

from controle.controlador_principal import ControladorPrincipal


if __name__ == "__main__":
    if "--exemplo" in sys.argv:
        import dados_exemplo
        dados_exemplo.ativar()
    ControladorPrincipal().iniciar()
