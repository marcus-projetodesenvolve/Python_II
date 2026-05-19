"""
main.py - Interface de linha de comando do pacote personalizador.

Uso:
    python main.py "texto" [-a] -m <modulo> -f <funcao>

Módulos disponíveis (-m):
    1 ou layout    - Funcionalidades de layout
    2 ou painel    - Funcionalidades de painel
    3 ou progresso - Funcionalidades de progresso
    4 ou estilo    - Funcionalidades de estilo

Funções por módulo (-f):
    layout:    1=exibir_colunas, 2=exibir_tabela
    painel:    1=exibir_painel_simples, 2=exibir_painel_destaque
    progresso: 1=exibir_progresso_simples, 2=exibir_progresso_etapas
    estilo:    1=exibir_texto_colorido, 2=exibir_markdown
"""

import argparse
import sys
from personalizador import MODULOS


def main():
    parser = argparse.ArgumentParser(
        prog="personalizador",
        description="Formata e exibe texto usando a biblioteca Rich.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "texto",
        help="Texto a ser formatado ou caminho para um arquivo de texto (use -a para indicar arquivo).",
    )

    parser.add_argument(
        "-a", "--arquivo",
        action="store_true",
        help="Indica que o argumento 'texto' é o caminho para um arquivo de texto.",
    )

    parser.add_argument(
        "-m", "--modulo",
        required=True,
        help=(
            "Módulo a ser utilizado (por nome ou id):\n"
            "  1 ou layout    - Funcionalidades de layout\n"
            "  2 ou painel    - Funcionalidades de painel\n"
            "  3 ou progresso - Funcionalidades de progresso\n"
            "  4 ou estilo    - Funcionalidades de estilo"
        ),
    )

    parser.add_argument(
        "-f", "--funcao",
        required=True,
        help=(
            "Função do módulo a ser chamada (por nome ou id):\n"
            "  layout:    1=exibir_colunas       | 2=exibir_tabela\n"
            "  painel:    1=exibir_painel_simples | 2=exibir_painel_destaque\n"
            "  progresso: 1=exibir_progresso_simples | 2=exibir_progresso_etapas\n"
            "  estilo:    1=exibir_texto_colorido | 2=exibir_markdown"
        ),
    )

    args = parser.parse_args()

    # Resolver módulo
    modulo = MODULOS.get(args.modulo.lower())
    if modulo is None:
        print(f"Erro: módulo '{args.modulo}' não encontrado.")
        print("Módulos disponíveis: 1=layout, 2=painel, 3=progresso, 4=estilo")
        sys.exit(1)

    # Resolver função
    funcao = modulo.FUNCOES.get(args.funcao.lower())
    if funcao is None:
        print(f"Erro: função '{args.funcao}' não encontrada no módulo '{args.modulo}'.")
        print("Use -h para ver as funções disponíveis.")
        sys.exit(1)

    # Executar
    funcao(args.texto, args.arquivo)


if __name__ == "__main__":
    main()
