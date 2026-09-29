# The Dungeoneer - English Playtest Build
# Algorithms and Data Structures I

import random
from copy import deepcopy
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DO MAPA
# ============================================================

# Símbolos:
# # = parede
# . = espaço transitável
# B = bloqueio de pedras (teste de Força)
# F = fenda/abismo (teste de Agilidade)
# R = mecanismo lógico/rúnico (teste de Intelecto)
# V = ameaça física/química (teste de Vigor)
# A = fenômeno mágico (teste de Arcana)
# K = posição de uma das três chaves
# G = portão de saída
#
# IMPORTANTE PARA O TRABALHO:
# Esta é uma MATRIZ em Python: uma lista contendo várias listas.
MAPA_BASE = [
    list("###############"),
    list("#.....#....K..#"),
    list("#.###.#.#####.#"),
    list("#...#.#..V..#.#"),
    list("###.#.###F#.#.#"),
    list("#...#.....#...#"),
    list("#.#####.#.###.#"),
    list("#K....B.#.....#"),
    list("#.###.#.#####.#"),
    list("#...R.#A..K...#"),
    list("#####.#####.#G#"),
    list("#.............#"),
    list("###############"),
]

POSICAO_INICIAL = (1, 1)
ARQUIVO_RANKING = Path(__file__).with_name("ranking_en.txt")

DIRECOES = {
    "n": (-1, 0),
    "north": (-1, 0),
    "s": (1, 0),
    "south": (1, 0),
    "e": (0, 1),
    "east": (0, 1),
    "w": (0, -1),
    "west": (0, -1),
}

ATRIBUTOS = ["Strength", "Agility", "Vigor", "Arcana", "Intellect", "Presence"]


# ============================================================
# DADOS DO MUNDO
# ============================================================

# Pequenas descrições usadas em espaços sem evento específico.
# A ideia é evitar repetir sempre a mesma frase sem transformar
# cada movimento em um grande bloco de texto.
DESCRICOES_ALEATORIAS = [
    "The rock here is damp and cold. Drops fall somewhere you cannot locate.",
    "The corridor smells of wet earth and iron. Fresh fingernail marks scar the wall.",
    "A draft brushes past you, though there is no visible opening nearby.",
    "A thin layer of dust covers the floor. Something passed through here without leaving footprints.",
    "You hear stone scraping against stone somewhere far away. The sound stops when you stop.",
    "Small bones have been crushed between the stones. Strands of hair still cling to some of them.",
    "The wall to your right is strangely warm. The rest of the cavern remains freezing cold.",
    "A sweet, rotten smell fills the corridor for a few seconds, then vanishes as quickly as it came.",
    "The narrow passage forces you to move sideways. For a moment, the stone seems to press against your back.",
    "Dark stains mark the floor. They continue for several meters, then stop abruptly.",
    "You find a human tooth wedged into a crack in the stone, as though someone placed it there deliberately.",
    "The ceiling hangs low. Something scratched long, parallel lines into the rock above your head.",
    "A wet sound echoes behind you. When you turn, there is nothing but the path you came from.",
    "White fungi grow silently between the stones. They shrink back when your shadow passes over them.",
    "A small puddle reflects your face. The reflection takes a moment too long to copy your movement.",
    "The stone beneath your feet seems to vibrate faintly, as if an enormous machine were running far below.",
    "You hear something like breathing coming from a narrow crack in the wall.",
    "The corridor is filled with nearly invisible strands. They are not webs; they look like human hair.",
    "A strip of rotting cloth hangs from a ledge. Something dark and dry is still stuck to it.",
    "For a few seconds, you hear footsteps matching your own. They stop when you stand still.",
    "A crack runs across the wall. Something white retreats deeper inside when your light draws near.",
    "The air grows heavy. Pressure builds in your ears as though you were descending much deeper.",
    "The stones form a natural arch resembling ribs. You prefer not to look at it for long.",
    "A small pile of teeth rests in the corner. None of them seem to belong to the same animal.",
    "A thick root pierces the ceiling and disappears into the stone again. It pulses almost imperceptibly.",
    "The passage becomes too quiet. Even the sound of your own breathing seems muffled.",
    "You find three fresh scratches on the wall. A fourth ends in a smear of dried blood.",
    "A fly passes in front of your face. It is the first normal living thing you have seen in some time.",
    "The floor sinks slightly beneath your weight, as though there were a hollow space directly below.",
    "Something brushes your ankle. When you recoil, you see only water running between the stones.",
    "There is a handprint on the wall. The fingers are far too long to belong to a person.",
    "Something whispers very softly behind the stones. You cannot make out any words.",
    "The ceiling disappears into darkness for several meters before closing over the corridor again.",
    "A thin stream of water runs down the wall. The water is clear, but leaves a reddish stain on the stone.",
    "You pass a carefully stacked pile of stones. A small bone rests on top.",
    "The air tastes metallic here. Your tongue tingles for a few moments.",
    "A shadow crosses the far end of the corridor. No footsteps accompany it.",
    "Dozens of small circles have been carved into the rock. Each has a dot at its center, like an eye.",
    "You hear a distant sob. A few seconds later, it repeats in exactly the same way.",
    "The passage is wide, yet you feel a strange need to walk directly through its center.",
]

def descricao_ambiente_aleatoria():
    return random.choice(DESCRICOES_ALEATORIAS)


OBSERVACOES_ALEATORIAS = [
    "The passage continues into the gloom. You notice no immediate movement.",
    "The path looks clear, though darkness hides whatever lies a few steps ahead.",
    "You see only uneven stone and shadows. Nothing moves, for now.",
    "The corridor continues ahead. A distant sound echoes and fades before you can identify its source.",
    "The passage is open. Something in the smell of the air makes you hesitate.",
    "Nothing blocks the way, but the silence ahead feels deliberate.",
    "Darkness swallows the passage after a few meters. You see nothing approaching.",
    "The path is clear. Small fragments of stone slide across the floor on their own farther ahead.",
    "You see no immediate obstacle. Even so, something makes your stomach tighten.",
    "The passage looks safe enough to cross. Down here, that does not mean much.",
]

DESCRICOES = {
    (1, 1): (
        "The entrance collapses behind you with a dry crack. "
        "The staircase you descended now ends beneath tons of rock. "
        "The air smells of rust, wet earth, and something faintly too sweet."
    ),
    (3, 5): (
        "A niche has been carved into the wall. Inside rests a short blade, "
        "covered in a dark crust you would rather believe is rust."
    ),
    (1, 11): (
        "The ceiling opens into a tall chamber. Ropes of roots descend from the darkness "
        "and coil around a pedestal made of calcified vertebrae."
    ),
    (3, 1): (
        "You find the remains of an old camp. The fabric of the packs "
        "has turned to dust, but a vial remains intact among human ribs."
    ),
    (3, 7): (
        "The walls stop being cut stone and become natural rock. "
        "Something carved parallel grooves into the floor, as if it had been dragged through here again and again."
    ),
    (3, 9): (
        "A greenish mist crawls along the floor. Tiny insects lie motionless within it, "
        "their legs twisted against their bodies. Breathing here seems like a bad idea."
    ),
    (3, 10): (
        "Wet tracks mark the floor. They begin small and human, "
        "but each successive footprint has longer toes than the one before it."
    ),
    (4, 9): (
        "A black chasm cuts across the path. Below, there is no sound of water, stone, or wind. "
        "Only a low, rhythmic sound, like breathing."
    ),
    (5, 5): (
        "A row of human teeth has been pressed into the mortar of the wall. "
        "They all point toward the same corridor."
    ),
    (5, 7): (
        "A corpse still wears an almost intact iron mail shirt. "
        "The body inside seems to have been squeezed until it fit into half its original size."
    ),
    (7, 1): (
        "At the bottom of a dry cistern lies a black key. "
        "Dozens of broken fingernails remain embedded in the stones around it."
    ),
    (7, 6): (
        "Collapsed stones choke the passage. Between them, you can see pieces of a hand "
        "still twitching slowly, though the rest of the body is nowhere in sight."
    ),
    (9, 4): (
        "A stone arch seals the corridor. Runes cover its surface, "
        "but they do not glow: they look like deep cuts that continue to bleed."
    ),
    (9, 7): (
        "Bluish symbols float a few centimeters above the stone, moving like worms beneath glass. "
        "You feel pressure behind your eyes when you try to focus on them."
    ),
    (9, 8): (
        "A sword rests upon a cracked altar. The blade is far too clean for this place."
    ),
    (9, 10): (
        "A small translucent key floats a few centimeters above the floor. "
        "Inside it, something resembling a pupil follows your movements."
    ),
    (10, 13): (
        "Before you stands the Raven Gate. Three locks form a triangle "
        "at the center of the door. A current of cold air comes from the other side: the first proof "
        "that the outside world still exists."
    ),
    (11, 6): (
        "The corridor widens unnaturally. Bones have been arranged in concentric circles. "
        "Something enormous sleeps among them, covered by a cloak made of stitched skin."
    ),
    (11, 11): (
        "A perfectly still pool of water reflects a ceiling that does not exist. "
        "In the reflection, someone is standing behind you."
    ),
}

PREVISOES = {
    (3, 5): "You make out the dull glint of a small blade inside a niche.",
    (1, 11): "There is an open chamber ahead, with something hanging above a pedestal.",
    (3, 9): "A greenish mist fills the passage. The smell is sharp and sickly sweet.",
    (3, 10): "You see wet footprints disappearing into the darkness.",
    (4, 9): "The floor ends abruptly. A wide chasm cuts across the path.",
    (5, 7): "There is a body covered in metal on the floor.",
    (7, 1): "You make out the shape of a dry cistern and something dark at the bottom.",
    (7, 6): "The passage appears to be blocked by a cave-in.",
    (9, 4): "An arch covered in inscriptions blocks the way.",
    (9, 7): "Glowing symbols move across the wall without ever staying in the same place.",
    (9, 8): "Something metallic rests on a stone surface.",
    (9, 10): "A glasslike gleam hangs suspended in the air.",
    (10, 13): "A monumental door bears three locks.",
    (11, 6): (
        "You smell the suffocating stench of old blood. "
        "Something very large seems to be breathing ahead. Going forward would be a conscious choice."
    ),
    (2, 5): (
    "You hear dozens of tiny claws scratching against the stone ahead. "
    "In the gloom, the floor seems to ripple."
    )
}


ITENS_INICIAIS = {
    (3, 5): [
        {"nome": "Rusty Dagger", "tipo": "arma", "dado": (1, 6),
         "descricao": "A short dagger. Damage: 1d6."}
    ],
    (1, 11): [
        {"nome": "Bone Key", "tipo": "chave",
         "descricao": "One of the three keys to the Raven Gate."}
    ],
    (3, 1): [
        {"nome": "Health Potion", "tipo": "cura", "dado": (1, 6),
         "descricao": "Restores 1d6 Health."}
    ],
    (5, 7): [
        {"nome": "Iron Mail", "tipo": "armadura", "reducao": 1,
         "descricao": "Reduces incoming physical damage dice by 1 step."}
    ],
    (7, 1): [
        {"nome": "Black Key", "tipo": "chave",
         "descricao": "One of the three keys to the Raven Gate."}
    ],
    (8, 5): [
        {"nome": "Mana Potion", "tipo": "mana", "dado": (1, 6),
         "descricao": "Restores 1d6 Mana."}
    ],
    (9, 8): [
        {"nome": "Altar Sword", "tipo": "arma", "dado": (1, 8),
         "descricao": "A strangely pristine sword. Damage: 1d8."}
    ],
    (9, 10): [
        {"nome": "Glass Key", "tipo": "chave",
         "descricao": "One of the three keys to the Raven Gate."}
    ],
    (11, 6): [
        {"nome": "Jailer's Shield", "tipo": "escudo", "reducao": 1,
         "descricao": "Reduces incoming physical damage dice by 1 additional step."}
    ],
}


INIMIGOS_INICIAIS = {
    (2, 5): {
    "nome": "Rat Swarm",
    "vida": 5,
    "dano": (1, 4),
    "terrivel": False,
    "descricao": (
        "The floor seems to move before you realize why. "
        "Dozens of rats pour from the cracks, far too thin, their fur plastered to their bodies with filth and blood. "
        "Some have milky white eyes; others have no eyes at all. "
        "They crawl over one another, forming a living mass of teeth and tails."
    ),
    "mensagem_derrota": (
        "The mass comes apart in desperate squeals. "
        "Some rats vanish into the cracks, while the rest "
        "form a layer of motionless bodies across the stone."
    ),
    "pontos": 20,
    },
    (3, 10): {
        "nome": "Pale Crawler",
        "vida": 12,
        "dano": (1, 6),
        "terrivel": False,
        "descricao": (
            "A child-sized creature crawls out from behind the rock. "
            "It moves on four human limbs, but every knee bends the wrong way. "
            "Its head has no eyes. Even so, it looks directly at you."
        ),
        "mensagem_derrota": (
            "The Pale Crawler collapses onto its side, its limbs still twitching at impossible angles. "
            "Even while motionless, its head remains turned toward you for several seconds before finally going slack."
),
        "pontos": 40,
    },
    (11, 6): {
        "nome": "Faceless Jailer",
        "vida": 24,
        "dano": (2, 8),
        "terrivel": True,
        "descricao": (
            "The mass beneath the cloak rises. It is too tall to stand upright in the corridor. "
            "Where a face should be, there is only smooth skin stitched shut with black thread. "
            "Four arms emerge from its torso, and each hand ends in fingers covered with tiny mouths."
        ),
        "mensagem_derrota": (
            "The Faceless Jailer staggers, as though its own body takes a moment to understand that it is dead. "
            "The tiny mouths on its fingers open one final time, releasing a low, wet chorus. "
            "Then the creature collapses among the bones and does not rise again."
),
        "pontos": 150,
    },
}


# ============================================================
# FUNÇÕES DE DADOS
# ============================================================

def rolar_dado(lados):
    return random.randint(1, lados)


def rolar_dados(quantidade, lados):
    return [rolar_dado(lados) for _ in range(quantidade)]


def texto_dado(dado):
    quantidade, lados = dado
    return f"{quantidade}d{lados}"


def dano_total(dado):
    quantidade, lados = dado
    return sum(rolar_dados(quantidade, lados))


# Ordem dos degraus damage.
DEGRAUS_DANO = [4, 6, 8, 10, 12, 20]


def reduzir_dado(dado, reducoes):
    """
    Reduz cada dado do ataque por degraus.
    Exemplo: 2d8 com 1 redução -> 2d6.
    Se a proteção passar abaixo de d4, o dano vira 0.
    """
    quantidade, lados = dado

    if reducoes <= 0:
        return dado

    try:
        indice = DEGRAUS_DANO.index(lados)
    except ValueError:
        return dado

    novo_indice = indice - reducoes
    if novo_indice < 0:
        return (0, 0)

    return (quantidade, DEGRAUS_DANO[novo_indice])


# ============================================================
# PERSONAGEM
# ============================================================

def criar_personagem():
    print("\n=== CHARACTER CREATION ===")
    nome = input("Adventurer's name: ").strip() or "Nameless"

    atributos = {atributo: 1 for atributo in ATRIBUTOS}
    pontos = 5

    print("\nAll attributes begin at 1.")
    print("Distribute 5 additional points. Starting maximum: 3.\n")

    while pontos > 0:
        mostrar_atributos(atributos)
        print(f"Points remaining: {pontos}")
        escolha = input("Attribute to increase: ").strip().lower()

        atributo_encontrado = None
        for atributo in ATRIBUTOS:
            if atributo.lower().startswith(escolha):
                atributo_encontrado = atributo
                break

        if atributo_encontrado is None:
            print("Invalid attribute.\n")
            continue

        if atributos[atributo_encontrado] >= 3:
            print("That attribute is already at the starting maximum.\n")
            continue

        atributos[atributo_encontrado] += 1
        pontos -= 1
        print()

    vida_max = 10 + atributos["Vigor"] * 5
    mana_max = 5 + atributos["Arcana"] * 4

    return {
        "nome": nome,
        "atributos": atributos,
        "vida": vida_max,
        "vida_max": vida_max,
        "mana": mana_max,
        "mana_max": mana_max,
        "posicao": POSICAO_INICIAL,
        "inventario": [],
        "arma": None,
        "armadura": None,
        "escudo": None,
        "chaves": 0,
        "pontos": 0,
    }


def mostrar_atributos(atributos):
    print(" | ".join(f"{nome}: {valor}" for nome, valor in atributos.items()))


def mostrar_status(jogador):
    arma = jogador["arma"]["nome"] if jogador["arma"] else "Improvised (1d4)"
    armadura = jogador["armadura"]["nome"] if jogador["armadura"] else "None"
    escudo = jogador["escudo"]["nome"] if jogador["escudo"] else "None"

    print("\n=== STATUS ===")
    print(f"Name: {jogador['nome']}")
    print(f"Health: {jogador['vida']}/{jogador['vida_max']}")
    print(f"Mana: {jogador['mana']}/{jogador['mana_max']}")
    print(f"Keys: {jogador['chaves']}/3")
    print(f"Score: {jogador['pontos']}")
    mostrar_atributos(jogador["atributos"])
    print(f"Weapon: {arma}")
    print(f"Armor: {armadura}")
    print(f"Shield: {escudo}")


def dado_arma(jogador):
    if jogador["arma"]:
        return jogador["arma"]["dado"]
    return (1, 4)


def reducao_defesa(jogador):
    reducao = 0
    if jogador["armadura"]:
        reducao += jogador["armadura"].get("reducao", 0)
    if jogador["escudo"]:
        reducao += jogador["escudo"].get("reducao", 0)
    return reducao


# ============================================================
# TESTES DE ATRIBUTO
# ============================================================

def teste_atributo(jogador, atributo, dificuldade):
    quantidade = jogador["atributos"][atributo]
    resultados = rolar_dados(quantidade, 20)
    melhor = max(resultados)

    print(f"\n[{atributo.upper()}] Difficulty: {dificuldade}")
    print(f"Rolls ({quantidade}d20): {resultados}")
    print(f"Best result: {melhor}")

    if melhor >= dificuldade:
        print("SUCCESS.")
        return True

    print("FAILURE.")
    return False


# ============================================================
# INVENTÁRIO E ITENS
# ============================================================

def listar_inventario(jogador):
    print("\n=== INVENTORY ===")
    if not jogador["inventario"]:
        print("Your inventory is empty.")
        return

    for i, item in enumerate(jogador["inventario"], start=1):
        print(f"{i}. {item['nome']} - {item['descricao']}")


def pegar_itens(jogador, itens_no_mapa):
    pos = jogador["posicao"]
    itens = itens_no_mapa.get(pos, [])

    if not itens:
        print("There is nothing here you can take.")
        return

    while itens:
        item = itens.pop(0)
        jogador["inventario"].append(item)
        print(f"You took: {item['nome']}.")

        if item["tipo"] == "chave":
            jogador["chaves"] += 1
            jogador["pontos"] += 100
            print(f"Keys found: {jogador['chaves']}/3.")

    if not itens:
        itens_no_mapa.pop(pos, None)


def encontrar_item(jogador, trecho_nome):
    trecho_nome = trecho_nome.lower()
    for item in jogador["inventario"]:
        if trecho_nome in item["nome"].lower():
            return item
    return None


def equipar_item(jogador, trecho_nome):
    item = encontrar_item(jogador, trecho_nome)

    if not item:
        print("You do not have that item.")
        return

    if item["tipo"] == "arma":
        jogador["arma"] = item
        print(f"You equipped {item['nome']}. Damage now: {texto_dado(item['dado'])}.")
    elif item["tipo"] == "armadura":
        jogador["armadura"] = item
        print(f"You put on {item['nome']}.")
    elif item["tipo"] == "escudo":
        jogador["escudo"] = item
        print(f"You equipped {item['nome']}.")
    else:
        print("That item cannot be equipped.")


def usar_item(jogador, trecho_nome):
    item = encontrar_item(jogador, trecho_nome)

    if not item:
        print("You do not have that item.")
        return

    if item["tipo"] == "cura":
        quantidade, lados = item["dado"]
        cura = dano_total((quantidade, lados))
        antes = jogador["vida"]
        jogador["vida"] = min(jogador["vida_max"], jogador["vida"] + cura)
        jogador["inventario"].remove(item)
        print(f"You recovered {jogador['vida'] - antes} Health.")
    elif item["tipo"] == "mana":
        quantidade, lados = item["dado"]
        cura = dano_total((quantidade, lados))
        antes = jogador["mana"]
        jogador["mana"] = min(jogador["mana_max"], jogador["mana"] + cura)
        jogador["inventario"].remove(item)
        print(f"You recovered {jogador['mana'] - antes} Mana.")
    else:
        print("That item is not consumable.")


# ============================================================
# MAPA, OBSERVAÇÃO E MOVIMENTO
# ============================================================

def dentro_do_mapa(linha, coluna):
    return 0 <= linha < len(MAPA_BASE) and 0 <= coluna < len(MAPA_BASE[0])


def posicao_na_direcao(posicao, direcao):
    if direcao not in DIRECOES:
        return None
    dl, dc = DIRECOES[direcao]
    return posicao[0] + dl, posicao[1] + dc


def observar_direcao(jogador, direcao, inimigos, paredes_conhecidas):
    destino = posicao_na_direcao(jogador["posicao"], direcao)

    if destino is None:
        print("Invalid direction. Use north, south, east, or west.")
        return

    linha, coluna = destino
    if not dentro_do_mapa(linha, coluna):
        print("There is no path in that direction.")
        return

    if MAPA_BASE[linha][coluna] == "#":
        paredes_conhecidas.add((linha, coluna))
        print("There is only stone ahead. No passage.")
        return

    print("\nYou remain where you are and look carefully...")

    if destino in PREVISOES:
        print(PREVISOES[destino])
    else:
        simbolo = MAPA_BASE[linha][coluna]
        if simbolo == "B":
            print("The passage is blocked by heavy stones.")
        elif simbolo == "F":
            print("The path appears to be cut off by a chasm.")
        elif simbolo == "R":
            print("You make out ancient inscriptions on a stone structure.")
        elif simbolo == "V":
            print("An unhealthy mist fills the path. Your body reacts before you even step inside.")
        elif simbolo == "A":
            print("There are arcane symbols ahead. They seem to change whenever you try to focus on them.")
        elif simbolo == "G":
            print("A monumental structure blocks the way.")
        else:
            print(random.choice(OBSERVACOES_ALEATORIAS))

    if destino in inimigos and inimigos[destino]["vida"] > 0:
        inimigo = inimigos[destino]
        if inimigo["terrivel"]:
            print("And there is something alive in there. Far too large. You can still choose not to enter.")
        else:
            print("You notice movement ahead.")


def descrever_local(jogador, itens_no_mapa, inimigos, descricoes_geradas):
    pos = jogador["posicao"]

    print("\n" + "=" * 60)

    if pos in DESCRICOES:
        print(DESCRICOES[pos])
    else:
        if pos not in descricoes_geradas:
            descricoes_geradas[pos] = random.choice(DESCRICOES_ALEATORIAS)

        print(descricoes_geradas[pos])

    if pos in itens_no_mapa and itens_no_mapa[pos]:
        nomes = ", ".join(item["nome"] for item in itens_no_mapa[pos])
        print(f"\nYou notice something that can be taken: {nomes}.")

    if pos in inimigos and inimigos[pos]["vida"] > 0:
        print("\nThere is a creature here.")


def tentar_obstaculo(jogador, simbolo, obstaculos_resolvidos, destino):
    if destino in obstaculos_resolvidos:
        return True

    if simbolo == "B":
        print("\nA cave-in blocks the passage.")
        print("[STRENGTH] Force a way through the stones.")
        if teste_atributo(jogador, "Strength", 11):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 20
            print("You force the stones aside until a narrow passage opens.")
            return True

        dano = rolar_dado(4)
        jogador["vida"] -= dano
        print(f"A stone crashes onto your shoulder. You lose {dano} Health.")
        return False

    if simbolo == "F":
        print("\nA wide chasm cuts across the path.")
        print("[AGILITY] Jump to the other side.")
        if teste_atributo(jogador, "Agility", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 20
            print("You leap and reach the opposite side.")
            return True

        dano = rolar_dado(6)
        jogador["vida"] -= dano
        print(
            f"You slip, slam against the rock, and manage to pull yourself back. "
            f"You lose {dano} Health."
        )
        return False

    if simbolo == "R":
        print("\nThe runes seal the passage like a scarred-over wound.")
        print("This mechanism requires reasoning; brute force has nowhere to take hold.")
        if teste_atributo(jogador, "Intellect", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 25
            print("You identify the correct sequence. The stone opens with a groan.")
            return True

        dano = rolar_dado(4)
        jogador["mana"] = max(0, jogador["mana"] - dano)
        print(f"The runes react to your attempt. You lose {dano} Mana.")
        return False

    if simbolo == "V":
        print("\nA poisonous mist fills the corridor.")
        print("[VIGOR] Hold your breath and cross before the poison paralyzes your muscles.")
        if teste_atributo(jogador, "Vigor", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 25
            print(
                "Your throat burns and your eyes water, but your body endures. "
                "You cross before the mist can overwhelm you."
            )
            return True

        dano = rolar_dado(6)
        jogador["vida"] -= dano
        print(
            f"Your muscles suddenly lock. You drop to your knees and can only "
            f"drag yourself back when the effect begins to fade. You lose {dano} Health."
        )
        return False

    if simbolo == "A":
        print("\nArcane symbols move across the stone like living organisms.")
        print("[ARCANA] Study the magical pattern and determine how to cross without triggering it.")
        if teste_atributo(jogador, "Arcana", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 30
            print(
                "You realize the runes do not form words, but a sequence of magical pulses. "
                "By synchronizing your steps with the pattern, the pressure in the air disappears."
            )
            return True

        perda_mana = rolar_dado(6)
        dano = rolar_dado(4)
        jogador["mana"] = max(0, jogador["mana"] - perda_mana)
        jogador["vida"] -= dano
        print(
            f"You misread the flow. The magic cuts through your thoughts like a blade. "
            f"You lose {perda_mana} Mana and {dano} Health."
        )
        return False

    return True


# ============================================================
# COMBATE
# ============================================================

def combate(jogador, inimigo):
    print("\n" + "!" * 60)
    print(inimigo["descricao"])
    print(f"\nENEMY: {inimigo['nome']}")
    print(f"Health: {inimigo['vida']} | Damage: {texto_dado(inimigo['dano'])}")

    if inimigo["terrivel"]:
        print(
            "\nThis does not look like a fair fight. Scourges are meant to "
            "be faced with good equipment. Fleeing remains an option."
        )

    while inimigo["vida"] > 0 and jogador["vida"] > 0:
        print(
            f"\nYour Health: {jogador['vida']}/{jogador['vida_max']} | "
            f"Mana: {jogador['mana']}/{jogador['mana_max']}"
        )
        print("Actions: attack | magic | flee | use <item>")
        acao = input("> ").strip().lower()

        if acao == "attack":
            dado = dado_arma(jogador)
            dano = dano_total(dado)
            inimigo["vida"] -= dano
            print(f"You attack with {texto_dado(dado)} and deal {dano} damage.")

        elif acao == "magic":
            custo = 3
            if jogador["mana"] < custo:
                print("Not enough Mana.")
                continue
            jogador["mana"] -= custo
            dano = dano_total((1, 8))
            inimigo["vida"] -= dano
            print(f"The arcane blast deals {dano} damage. (-{custo} Mana)")

        elif acao.startswith("use "):
            usar_item(jogador, acao[4:].strip())
            continue

        elif acao == "flee":
            custo = rolar_dado(4)
            jogador["vida"] = max(1, jogador["vida"] - custo)
            print(
                f"You retreat in panic and injure yourself while fleeing. You lose {custo} Health, "
                "but remain alive."
            )
            return "fled"

        else:
            print("Invalid action.")
            continue

        if inimigo["vida"] <= 0:
            print(f"\n{inimigo['mensagem_derrota']}")
            jogador["pontos"] += inimigo["pontos"]
            return "won"

        # Turno do inimigo
        reducoes = reducao_defesa(jogador)
        dado_reduzido = reduzir_dado(inimigo["dano"], reducoes)

        if dado_reduzido == (0, 0):
            print(
                f"{inimigo['nome']} attacks, but your protection completely absorbs the blow."
            )
        else:
            dano = dano_total(dado_reduzido)
            jogador["vida"] -= dano
            print(
                f"{inimigo['nome']} attacks. Your defense reduces "
                f"{texto_dado(inimigo['dano'])} to {texto_dado(dado_reduzido)}. "
                f"You suffer {dano} damage."
            )

    return "dead"


# ============================================================
# MAPA DESCOBERTO
# ============================================================

def mostrar_mapa_descoberto(jogador, visitados, paredes_conhecidas):
    print("\n=== EXPLORED MAP ===")
    print("@ = you | · = visited location | ■ = discovered wall | ? = unknown")

    for linha in range(len(MAPA_BASE)):
        exibicao = []

        for coluna in range(len(MAPA_BASE[linha])):
            pos = (linha, coluna)

            if pos == jogador["posicao"]:
                exibicao.append("@")
            elif pos in paredes_conhecidas:
                exibicao.append("■")
            elif pos in visitados:
                exibicao.append("·")
            else:
                exibicao.append("?")

        print("".join(exibicao))


# ============================================================
# RANKING
# ============================================================

def salvar_pontuacao(jogador, resultado):
    linha = f"{jogador['nome']};{jogador['pontos']};{resultado}\n"
    with ARQUIVO_RANKING.open("a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def mostrar_ranking():
    print("\n=== RANKING ===")

    if not ARQUIVO_RANKING.exists():
        print("There are no saved scores yet.")
        return

    registros = []

    with ARQUIVO_RANKING.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) != 3:
                continue

            nome, pontos, resultado = partes
            try:
                registros.append((nome, int(pontos), resultado))
            except ValueError:
                continue

    registros.sort(key=lambda item: item[1], reverse=True)

    if not registros:
        print("There are no valid scores yet.")
        return

    for posicao, (nome, pontos, resultado) in enumerate(registros[:10], start=1):
        print(f"{posicao:>2}. {nome:<20} {pontos:>4} pts  ({resultado})")


# ============================================================
# JOGO PRINCIPAL
# ============================================================

def ajuda():
    print("""
=== COMMANDS ===
n / north              move north
s / south              move south
e / east               move east
w / west               move west

look north             inspect before entering
look south
look east
look west

examine                inspect the current location again
take                   take items from the current location
inventory              show your items
equip <item>           equip a weapon, armor, or shield
use <item>             use a potion
status                 show character sheet
map                    show only explored areas
help                   show this list
quit                   abandon the run
""")


def jogar():
    jogador = criar_personagem()
    itens_no_mapa = deepcopy(ITENS_INICIAIS)
    inimigos = deepcopy(INIMIGOS_INICIAIS)
    obstaculos_resolvidos = set()
    visitados = {POSICAO_INICIAL}
    paredes_conhecidas = set()
    descricoes_geradas = {}

    print("\n" + "=" * 60)
    print("THE DUNGEONEER")
    print("=" * 60)
    print(
        "You awaken beneath Myrthwa, somewhere between the dungeon of the ancient kings "
        "and the caves that existed long before them.\n"
        "They say three keys open the only gate to the surface.\n"
        "They also say no one who found all three ever returned to confirm it."
    )

    descrever_local(
    jogador,
    itens_no_mapa,
    inimigos,
    descricoes_geradas
)
    ajuda()

    while jogador["vida"] > 0:
        comando = input("\n> ").strip().lower()

        if not comando:
            continue

        if comando in DIRECOES:
            destino = posicao_na_direcao(jogador["posicao"], comando)
            linha, coluna = destino

            if not dentro_do_mapa(linha, coluna):
                print("There is no path in that direction.")
                continue

            if MAPA_BASE[linha][coluna] == "#":
                paredes_conhecidas.add((linha, coluna))
                print("Solid stone completely blocks that path.")
                continue

            simbolo = MAPA_BASE[linha][coluna]

            if not tentar_obstaculo(
                jogador, simbolo, obstaculos_resolvidos, destino
            ):
                if jogador["vida"] <= 0:
                    break
                continue

            # O portão só pode ser atravessado com as três chaves.
            if simbolo == "G":
                if jogador["chaves"] < 3:
                    print(
                        f"The Raven Gate has three locks. "
                        f"You carry only {jogador['chaves']} key(s)."
                    )
                    continue

                jogador["posicao"] = destino
                visitados.add(destino)
                descrever_local(
    jogador,
    itens_no_mapa,
    inimigos,
    descricoes_geradas
)
                jogador["pontos"] += 250
                print(
                    "\nThe three keys turn at the same time.\n"
                    "The gate opens and, for the first time in hours, you feel real wind.\n"
                    "Behind you, something begins running through the corridors.\n"
                    "You do not look back.\n\n"
                    "YOU ESCAPED THE DUNGEON."
                )
                salvar_pontuacao(jogador, "ESCAPED")
                print(f"Final score: {jogador['pontos']}")
                return

            posicao_anterior = jogador["posicao"]
            jogador["posicao"] = destino
            visitados.add(destino)
            descrever_local(
    jogador,
    itens_no_mapa,
    inimigos,
    descricoes_geradas
)

            # Combate ao entrar em um local ocupado.
            if destino in inimigos and inimigos[destino]["vida"] > 0:
                resultado = combate(jogador, inimigos[destino])

                if resultado == "fled":
                    jogador["posicao"] = posicao_anterior
                    print("You return to the previous passage.")
                elif resultado == "dead":
                    break

        elif comando.startswith("look "):
            direcao = comando[5:].strip()
            observar_direcao(jogador, direcao, inimigos, paredes_conhecidas)

        elif comando == "examine":
            descrever_local(
    jogador,
    itens_no_mapa,
    inimigos,
    descricoes_geradas
)

        elif comando in ("take", "take item", "take items"):
            pegar_itens(jogador, itens_no_mapa)

        elif comando == "inventory":
            listar_inventario(jogador)

        elif comando.startswith("equip "):
            equipar_item(jogador, comando[6:].strip())

        elif comando.startswith("use "):
            usar_item(jogador, comando[4:].strip())

        elif comando == "status":
            mostrar_status(jogador)

        elif comando == "map":
            mostrar_mapa_descoberto(jogador, visitados, paredes_conhecidas)

        elif comando == "help":
            ajuda()

        elif comando == "quit":
            print("You abandon the expedition.")
            salvar_pontuacao(jogador, "ABANDONED")
            return

        else:
            print("Unknown command. Type 'help' to see the commands.")

    print(
        "\nYour legs give out. The last thing you hear is something approaching "
        "slowly, as though it knows there is no longer any reason to run."
    )
    print("\nYOU DIED.")
    salvar_pontuacao(jogador, "DIED")
    print(f"Final score: {jogador['pontos']}")


def menu():
    while True:
        print("\n" + "=" * 60)
        print("THE DUNGEONEER - PROTOTYPE")
        print("=" * 60)
        print("1. Play")
        print("2. View ranking")
        print("3. Quit")

        escolha = input("> ").strip()

        if escolha == "1":
            jogar()
        elif escolha == "2":
            mostrar_ranking()
        elif escolha == "3":
            print("Until next time.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
