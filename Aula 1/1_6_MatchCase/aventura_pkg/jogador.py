"""
Módulo jogador - controle de movimentação e pontuação.

Funções:
    iniciar_jogador(lab)          -> dict
    mover(jogador, lab, tecla)    -> str
    pontuar(jogador, evento)
    resolver_labirinto(lab, pos)  -> list  [RECURSIVA]
"""

from rich.console import Console
from aventura_pkg.labirinto import PAREDE, SAIDA, ITEM

console = Console()

TECLAS = {
    "w": (-1,  0),
    "s": ( 1,  0),
    "a": (  0, -1),
    "d": (  0,  1),
}


def iniciar_jogador(lab: list, nome: str = "Jogador") -> dict:
    """
    Cria o dicionário de estado do jogador na posição inicial (1,1).

    Args:
        lab  (list): Matriz do labirinto.
        nome (str) : Nome do jogador.

    Returns:
        dict: Estado do jogador com pos, pontuação, itens e movimentos.
    """
    return {
        "nome"      : nome,
        "pos"       : (1, 1),
        "pontos"    : 0,
        "itens"     : 0,
        "movimentos": 0,
        "venceu"    : False,
    }


def mover(jogador: dict, lab: list, tecla: str) -> str:
    """
    Move o jogador no labirinto de acordo com a tecla pressionada.

    Args:
        jogador (dict): Estado atual do jogador.
        lab     (list): Matriz do labirinto.
        tecla   (str) : Tecla pressionada ('w','a','s','d').

    Returns:
        str: Mensagem descrevendo o resultado do movimento.
    """
    if tecla not in TECLAS:
        return "Tecla inválida."

    dr, dc = TECLAS[tecla]
    r, c   = jogador["pos"]
    nr, nc = r + dr, c + dc

    if lab[nr][nc] == PAREDE:
        return "[red]Bloqueado![/red]"

    jogador["pos"] = (nr, nc)
    jogador["movimentos"] += 1

    celula = lab[nr][nc]
    if celula == ITEM:
        lab[nr][nc] = " "
        pontuar(jogador, "item")
        return "[magenta]★ Item coletado! +20 pontos[/magenta]"
    if celula == SAIDA:
        jogador["venceu"] = True
        pontuar(jogador, "saida")
        return "[bold yellow]🏆 Você encontrou a saída![/bold yellow]"

    return "Moveu."


def pontuar(jogador: dict, evento: str) -> None:
    """
    Atualiza a pontuação do jogador conforme o evento ocorrido.

    Eventos:
        'item'  -> +20 pontos
        'saida' -> +100 pontos - (movimentos * 2)
        'passo' -> -1 ponto

    Args:
        jogador (dict): Estado do jogador.
        evento  (str) : Tipo de evento.
    """
    match evento:
        case "item":
            jogador["pontos"] += 20
            jogador["itens"]  += 1
        case "saida":
            bonus = max(0, 100 - jogador["movimentos"] * 2)
            jogador["pontos"] += bonus
        case "passo":
            jogador["pontos"] = max(0, jogador["pontos"] - 1)


def resolver_labirinto(lab: list, pos: tuple, visitados: set = None) -> list:
    """
    Resolve o labirinto recursivamente a partir de uma posição.

    Percorre o labirinto usando DFS e retorna a lista de movimentos
    ('w','a','s','d') que levam da posição atual até a saída.

    Args:
        lab      (list) : Matriz do labirinto.
        pos      (tuple): Posição atual (linha, col).
        visitados(set)  : Conjunto de posições já visitadas.

    Returns:
        list: Sequência de teclas para resolver o labirinto, ou [] se sem solução.
    """
    if visitados is None:
        visitados = set()

    r, c = pos
    if lab[r][c] == SAIDA:
        return []

    visitados.add(pos)

    direcoes = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
    for tecla, (dr, dc) in direcoes.items():
        nr, nc = r + dr, c + dc
        nova   = (nr, nc)
        if nova not in visitados and lab[nr][nc] != PAREDE:
            resultado = resolver_labirinto(lab, nova, visitados)
            if resultado is not None:
                return [tecla] + resultado

    return None
