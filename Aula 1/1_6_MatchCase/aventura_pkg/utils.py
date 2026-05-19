"""
Módulo utils - utilitários de interface, animações e menus.

Funções:
    imprimir_instrucoes()
    imprimir_menu(nome, cor)              -> str
    tela_resultado(jogador, cor)
    animacao_vitoria(nome, nivel, cor)    [RECURSIVA]
    imprimir_hud(jogador)
"""

import time
from rich.console   import Console
from rich.panel     import Panel
from rich.text      import Text
from rich.table     import Table
from rich.align     import Align

console = Console()

INSTRUCOES = """
[bold cyan]═══════════════ COMO JOGAR ═══════════════[/bold cyan]

  [bold yellow]W[/bold yellow]  → Mover para cima
  [bold yellow]S[/bold yellow]  → Mover para baixo
  [bold yellow]A[/bold yellow]  → Mover para a esquerda
  [bold yellow]D[/bold yellow]  → Mover para a direita
  [bold yellow]Q[/bold yellow]  → Sair do jogo

  [bold magenta]★[/bold magenta]  → Itens coletáveis (+20 pontos cada)
  [bold yellow]E[/bold yellow]  → Saída do labirinto (objetivo!)
  [bold green]@[/bold green]  → Você (o jogador)

  [bold white]Pontuação:[/bold white]
    • Cada item coletado  → +20 pts
    • Chegar à saída      → +100 pts - (movimentos × 2)

[bold cyan]══════════════════════════════════════════[/bold cyan]
"""


def imprimir_instrucoes() -> None:
    """Exibe as instruções do jogo formatadas com Rich."""
    console.print(Panel(INSTRUCOES, title="[bold green]Aventura no Labirinto[/bold green]",
                        border_style="cyan", padding=(1, 4)))


def imprimir_menu(nome: str = "Jogador", cor: str = "green") -> str:
    """
    Exibe o menu principal e retorna a opção escolhida pelo usuário.

    Opções:
        1 - Jogar
        2 - Instruções
        3 - Assistir solução automática
        4 - Sair

    Args:
        nome (str): Nome do jogador para personalizar o menu.
        cor  (str): Cor principal do jogador.

    Returns:
        str: Opção escolhida ('1','2','3','4').
    """
    console.clear()
    titulo = Text("⚔  AVENTURA NO LABIRINTO  ⚔", style=f"bold {cor}", justify="center")
    console.print(Panel(Align.center(titulo), border_style=cor, padding=(1, 6)))
    console.print(f"\n  Olá, [bold {cor}]{nome}[/bold {cor}]! O que deseja fazer?\n")
    console.print("  [bold]1[/bold] → Jogar")
    console.print("  [bold]2[/bold] → Instruções")
    console.print("  [bold]3[/bold] → Assistir solução automática")
    console.print("  [bold]4[/bold] → Sair\n")

    while True:
        opcao = input("  Escolha (1-4): ").strip()
        if opcao in ("1", "2", "3", "4"):
            return opcao
        console.print("  [red]Opção inválida. Tente novamente.[/red]")


def imprimir_hud(jogador: dict, cor: str = "green") -> None:
    """
    Imprime a barra de informações do jogador (HUD) acima do labirinto.

    Args:
        jogador (dict): Estado atual do jogador.
        cor     (str) : Cor do jogador.
    """
    tabela = Table.grid(padding=(0, 2))
    tabela.add_row(
        f"[bold {cor}]{jogador['nome']}[/bold {cor}]",
        f"[yellow]★ Itens: {jogador['itens']}[/yellow]",
        f"[cyan]Pontos: {jogador['pontos']}[/cyan]",
        f"[dim]Movimentos: {jogador['movimentos']}[/dim]",
    )
    console.print(Panel(tabela, border_style=cor, padding=(0, 2)))


def tela_resultado(jogador: dict, cor: str = "green") -> None:
    """
    Exibe a tela de vitória ou derrota com estatísticas do jogador.

    Args:
        jogador (dict): Estado final do jogador.
        cor     (str) : Cor do jogador.
    """
    console.clear()
    if jogador["venceu"]:
        animacao_vitoria(jogador["nome"], 5, cor)
        msg = f"""
[bold yellow]🏆 PARABÉNS, {jogador['nome'].upper()}! VOCÊ VENCEU! 🏆[/bold yellow]

  [cyan]Itens coletados :[/cyan] {jogador['itens']}
  [cyan]Movimentos      :[/cyan] {jogador['movimentos']}
  [cyan]Pontuação final :[/cyan] [bold green]{jogador['pontos']}[/bold green]
"""
    else:
        msg = f"""
[bold red]💀 Fim de jogo, {jogador['nome']}. Melhor sorte próxima vez![/bold red]

  [cyan]Itens coletados :[/cyan] {jogador['itens']}
  [cyan]Movimentos      :[/cyan] {jogador['movimentos']}
  [cyan]Pontuação final :[/cyan] [bold]{jogador['pontos']}[/bold]
"""
    console.print(Panel(msg, border_style="yellow" if jogador["venceu"] else "red",
                        padding=(1, 4)))


def animacao_vitoria(nome: str, nivel: int, cor: str = "green") -> None:
    """
    Exibe uma animação recursiva de celebração de vitória.

    A cada nível imprime uma linha de estrelas crescente.
    Caso base: nivel == 0 (para a recursão).

    Args:
        nome  (str): Nome do jogador.
        nivel (int): Nível atual da animação (decrementado recursivamente).
        cor   (str): Cor da animação.
    """
    if nivel == 0:
        return
    estrelas = "★ " * nivel
    console.print(f"[bold {cor}]{estrelas.center(60)}[/bold {cor}]")
    time.sleep(0.12)
    animacao_vitoria(nome, nivel - 1, cor)
