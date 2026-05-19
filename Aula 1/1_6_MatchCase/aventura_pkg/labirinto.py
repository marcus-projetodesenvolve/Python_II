"""
Módulo labirinto - geração e impressão do labirinto.

Funções:
    criar_labirinto(largura, altura)  -> list[list[str]]
    imprimir_labirinto(lab, jog_pos)
    gerar_itens(lab)
"""

import random
from rich.console import Console

console = Console()

PAREDE  = "█"
CAMINHO = " "
ITEM    = "★"
SAIDA   = "E"


def criar_labirinto(largura: int = 21, altura: int = 11) -> list:
    """
    Gera um labirinto aleatório usando algoritmo de Recursive Backtracking.

    Args:
        largura (int): Número de colunas (deve ser ímpar). Padrão 21.
        altura  (int): Número de linhas  (deve ser ímpar). Padrão 11.

    Returns:
        list[list[str]]: Matriz 2D representando o labirinto.
    """
    # garantir dimensões ímpares
    if largura % 2 == 0:
        largura += 1
    if altura % 2 == 0:
        altura += 1

    lab = [[PAREDE] * largura for _ in range(altura)]

    def escavar(x, y):
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 1 <= nx < largura - 1 and 1 <= ny < altura - 1 and lab[ny][nx] == PAREDE:
                lab[y + dy // 2][x + dx // 2] = CAMINHO
                lab[ny][nx] = CAMINHO
                escavar(nx, ny)

    lab[1][1] = CAMINHO
    escavar(1, 1)

    # Saída no canto inferior direito
    lab[altura - 2][largura - 2] = SAIDA

    return lab


def gerar_itens(lab: list, quantidade: int = 3) -> list:
    """
    Insere itens coletáveis (★) em posições aleatórias de caminho no labirinto.

    Args:
        lab       (list): Matriz do labirinto.
        quantidade (int): Número de itens a inserir. Padrão 3.

    Returns:
        list: Lista de posições (linha, coluna) dos itens inseridos.
    """
    posicoes = []
    candidatos = [
        (r, c)
        for r in range(len(lab))
        for c in range(len(lab[0]))
        if lab[r][c] == CAMINHO and (r, c) != (1, 1)
    ]
    escolhidos = random.sample(candidatos, min(quantidade, len(candidatos)))
    for r, c in escolhidos:
        lab[r][c] = ITEM
        posicoes.append((r, c))
    return posicoes


def imprimir_labirinto(lab: list, jog_pos: tuple, nome: str = "Jogador", cor: str = "green") -> None:
    """
    Imprime o labirinto no terminal com Rich, destacando o jogador.

    Args:
        lab     (list) : Matriz do labirinto.
        jog_pos (tuple): Posição atual (linha, col) do jogador.
        nome    (str)  : Nome do jogador (exibido como símbolo).
        cor     (str)  : Cor do jogador no terminal.
    """
    jl, jc = jog_pos
    linhas = []
    for r, linha in enumerate(lab):
        row = ""
        for c, cel in enumerate(linha):
            if (r, c) == (jl, jc):
                row += f"[bold {cor}]@[/bold {cor}]"
            elif cel == PAREDE:
                row += "[bold white]█[/bold white]"
            elif cel == SAIDA:
                row += "[bold yellow]E[/bold yellow]"
            elif cel == ITEM:
                row += "[bold magenta]★[/bold magenta]"
            else:
                row += " "
        linhas.append(row)
    console.print("\n".join(linhas))
