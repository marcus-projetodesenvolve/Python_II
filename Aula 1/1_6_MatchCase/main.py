"""
main.py - Ponto de entrada do jogo Aventura no Labirinto.

Uso:
    python main.py [--name NOME] [--color COR] [--dificuldade N]
                   [--disable-sound] [--max-mov N]

Argumentos:
    --name NOME         Nome do(a) jogador(a) (padrão: Aventureiro)
    --color COR         Cor principal do jogo: green|cyan|magenta|yellow|red (padrão: green)
    --dificuldade N     Tamanho do labirinto: 1=pequeno, 2=médio, 3=grande (padrão: 2)
    --disable-sound     Desativa efeitos sonoros (playsound)
    --max-mov N         Limite máximo de movimentos (padrão: ilimitado)
"""

import argparse
import copy
import time

from rich.console import Console

from aventura_pkg import labirinto as lab_mod
from aventura_pkg import jogador   as jog_mod
from aventura_pkg import utils

console = Console()

TAMANHOS = {
    "1": (11, 7),
    "2": (21, 11),
    "3": (31, 17),
}

CORES_VALIDAS = ["green", "cyan", "magenta", "yellow", "red"]


def parse_args():
    """Configura e retorna os argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="aventura_no_labirinto",
        description="⚔  Aventura no Labirinto — explore, colete itens e encontre a saída!",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--name", default="Aventureiro",
        help="Nome do(a) jogador(a) (padrão: Aventureiro)"
    )
    parser.add_argument(
        "--color", default="green", choices=CORES_VALIDAS,
        help=f"Cor principal do jogo: {'|'.join(CORES_VALIDAS)} (padrão: green)"
    )
    parser.add_argument(
        "--dificuldade", default="2", choices=["1", "2", "3"],
        help="Tamanho do labirinto:\n  1 = pequeno\n  2 = médio (padrão)\n  3 = grande"
    )
    parser.add_argument(
        "--disable-sound", action="store_true",
        help="Desativa efeitos sonoros"
    )
    parser.add_argument(
        "--max-mov", type=int, default=0,
        help="Limite máximo de movimentos (0 = ilimitado, padrão: 0)"
    )
    return parser.parse_args()


def jogar(nome, cor, largura, altura, max_mov, sound):
    """Loop principal do jogo."""
    import pynput.keyboard as kb

    lab   = lab_mod.criar_labirinto(largura, altura)
    lab_mod.gerar_itens(lab, quantidade=4)
    jog   = jog_mod.iniciar_jogador(lab, nome)

    tecla_atual = [None]

    def on_press(key):
        try:
            tecla_atual[0] = key.char
        except AttributeError:
            pass

    listener = kb.Listener(on_press=on_press)
    listener.start()

    while not jog["venceu"]:
        console.clear()
        utils.imprimir_hud(jog, cor)
        lab_mod.imprimir_labirinto(lab, jog["pos"], nome, cor)

        if max_mov and jog["movimentos"] >= max_mov:
            console.print("[bold red]Limite de movimentos atingido![/bold red]")
            break

        # Aguardar tecla
        tecla_atual[0] = None
        while tecla_atual[0] not in ("w", "a", "s", "d", "q"):
            time.sleep(0.05)

        tecla = tecla_atual[0]
        if tecla == "q":
            break

        msg = jog_mod.mover(jog, lab, tecla)
        jog_mod.pontuar(jog, "passo")
        console.print(msg)
        time.sleep(0.05)

    listener.stop()
    utils.tela_resultado(jog, cor)


def assistir_solucao(nome, cor, largura, altura):
    """Modo de solução automática: o personagem resolve o labirinto sozinho."""
    import pynput.keyboard as kb

    lab     = lab_mod.criar_labirinto(largura, altura)
    lab_copia = copy.deepcopy(lab)
    jog     = jog_mod.iniciar_jogador(lab_copia, nome)

    movimentos = jog_mod.resolver_labirinto(lab_copia, (1, 1))

    if not movimentos:
        console.print("[red]Não foi possível resolver este labirinto.[/red]")
        return

    console.print(f"[cyan]Solução encontrada com {len(movimentos)} movimentos. Assistindo...[/cyan]")
    time.sleep(1)

    for tecla in movimentos:
        console.clear()
        utils.imprimir_hud(jog, cor)
        lab_mod.imprimir_labirinto(lab, jog["pos"], nome, cor)
        jog_mod.mover(jog, lab, tecla)
        time.sleep(0.18)

    console.clear()
    utils.imprimir_hud(jog, cor)
    lab_mod.imprimir_labirinto(lab, jog["pos"], nome, cor)
    console.print("[bold yellow]Solução concluída![/bold yellow]")
    time.sleep(1.5)


def main():
    """Função principal: inicializa args e controla o fluxo do jogo."""
    args = parse_args()

    nome      = args.name
    cor       = args.color
    largura, altura = TAMANHOS[args.dificuldade]
    max_mov   = args.max_mov
    sound     = not args.disable_sound

    while True:
        opcao = utils.imprimir_menu(nome, cor)

        match opcao:
            case "1":
                jogar(nome, cor, largura, altura, max_mov, sound)
                input("\n  Pressione ENTER para voltar ao menu...")
            case "2":
                console.clear()
                utils.imprimir_instrucoes()
                input("\n  Pressione ENTER para voltar ao menu...")
            case "3":
                assistir_solucao(nome, cor, largura, altura)
                input("\n  Pressione ENTER para voltar ao menu...")
            case "4":
                console.print(f"\n[bold {cor}]Até logo, {nome}! 👋[/bold {cor}]\n")
                break


if __name__ == "__main__":
    main()
