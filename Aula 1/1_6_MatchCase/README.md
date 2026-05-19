# ⚔ Aventura no Labirinto

Jogo de exploração de labirinto via terminal, desenvolvido em Python com as bibliotecas `rich` e `pynput`.

## 🎮 Como jogar

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o jogo
python main.py
python main.py --name "Marcus" --color cyan --dificuldade 3
python main.py --name "Marcus" --color magenta --max-mov 100
```

## ⚙️ Argumentos CLI

| Argumento | Descrição | Padrão |
|---|---|---|
| `--name NOME` | Nome do jogador | Aventureiro |
| `--color COR` | Cor: `green`, `cyan`, `magenta`, `yellow`, `red` | green |
| `--dificuldade N` | Tamanho: `1`=pequeno, `2`=médio, `3`=grande | 2 |
| `--disable-sound` | Desativa sons | False |
| `--max-mov N` | Limite de movimentos (0=ilimitado) | 0 |

## 🕹️ Controles

| Tecla | Ação |
|---|---|
| `W` | Mover para cima |
| `S` | Mover para baixo |
| `A` | Mover para a esquerda |
| `D` | Mover para a direita |
| `Q` | Sair do jogo |

## 📦 Estrutura do projeto

```
aventura_no_labirinto/
├── aventura_pkg/
│   ├── __init__.py
│   ├── labirinto.py   # geração e impressão do labirinto
│   ├── jogador.py     # movimentação, pontuação e solução recursiva
│   └── utils.py       # menus, HUD, animações e instruções
├── main.py            # CLI principal com argparse + match-case
├── requirements.txt
├── aventura_pkg.html  # documentação pydoc
└── README.md
```

## 🧩 Funcionalidades

- **Labirinto gerado aleatoriamente** a cada partida (Recursive Backtracking)
- **Itens coletáveis** (★) espalhados pelo labirinto (+20 pts cada)
- **Sistema de pontuação** baseado em itens coletados e movimentos
- **Solução automática recursiva** — assista o personagem resolver o labirinto
- **Animação de vitória recursiva** com estrelas crescentes
- **Interface colorida** com Rich (painéis, tabelas, HUD, menus)
