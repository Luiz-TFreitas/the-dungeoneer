# The Dungeoneer - Protótipo acadêmico
# Algoritmos e Estruturas de Dados I

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
ARQUIVO_RANKING = Path(__file__).with_name("ranking.txt")

DIRECOES = {
    "n": (-1, 0),
    "norte": (-1, 0),
    "s": (1, 0),
    "sul": (1, 0),
    "l": (0, 1),
    "leste": (0, 1),
    "o": (0, -1),
    "oeste": (0, -1),
}

ATRIBUTOS = ["Força", "Agilidade", "Vigor", "Arcana", "Intelecto", "Presença"]


# ============================================================
# DADOS DO MUNDO
# ============================================================

# Pequenas descrições usadas em espaços sem evento específico.
# A ideia é evitar repetir sempre a mesma frase sem transformar
# cada movimento em um grande bloco de texto.
DESCRICOES_ALEATORIAS = [
    "A rocha aqui está úmida e fria. Gotas caem em algum lugar que você não consegue localizar.",
    "O corredor cheira a terra molhada e ferro. Há marcas de unhas recentes na parede.",
    "Uma corrente de ar passa por você, embora não exista abertura visível por perto.",
    "O chão está coberto por uma camada fina de pó. Algo passou por aqui e não deixou pegadas.",
    "Você ouve pedra raspando contra pedra em algum ponto distante. O som para quando você para.",
    "Pequenos ossos estão esmagados entre as pedras. Alguns ainda possuem fios de cabelo presos a eles.",
    "A parede à sua direita é estranhamente morna. O restante da caverna continua gelado.",
    "Um cheiro doce e podre toma o corredor por alguns segundos e desaparece tão rápido quanto surgiu.",
    "A passagem estreita obriga você a andar de lado. Por um instante, parece que a pedra aperta suas costas.",
    "Há manchas escuras no chão. Elas continuam por alguns metros e terminam de forma abrupta.",
    "Você encontra um dente humano preso numa rachadura da pedra, como se alguém o tivesse colocado ali.",
    "O teto está baixo. Algo arranhou a rocha acima de sua cabeça em linhas longas e paralelas.",
    "Um ruído úmido ecoa atrás de você. Quando olha, não há nada além do caminho por onde veio.",
    "Fungos brancos crescem em silêncio entre as pedras. Eles se retraem quando sua sombra passa sobre eles.",
    "Uma pequena poça reflete seu rosto. O reflexo demora um instante a imitar seu movimento.",
    "A pedra sob seus pés parece vibrar levemente, como se uma máquina enorme funcionasse muito abaixo.",
    "Você percebe um som parecido com respiração vindo de uma fenda estreita na parede.",
    "O corredor está cheio de fios quase invisíveis. Não são teias; parecem cabelos humanos.",
    "Um pedaço de tecido apodrecido está preso numa saliência. Ainda há algo escuro e seco aderido a ele.",
    "Por alguns segundos, você escuta passos acompanhando os seus. Eles cessam quando você fica imóvel.",
    "Uma rachadura atravessa a parede. Dentro dela, alguma coisa branca desaparece quando sua luz se aproxima.",
    "O ar fica pesado. Você sente a pressão nos ouvidos como se estivesse descendo muito mais fundo.",
    "As pedras formam um arco natural que lembra costelas. Você prefere não olhar por muito tempo.",
    "Há um pequeno monte de dentes no canto da passagem. Nenhum deles parece pertencer ao mesmo animal.",
    "Uma raiz grossa atravessa o teto e entra novamente na pedra. Ela pulsa de forma quase imperceptível.",
    "A passagem fica silenciosa demais. Até o som da sua própria respiração parece abafado.",
    "Você encontra três riscos recentes na parede. Um quarto risco termina em uma mancha de sangue seco.",
    "Uma mosca passa por seu rosto. É a primeira coisa viva e normal que você vê há algum tempo.",
    "O chão afunda levemente sob seu peso, como se houvesse um espaço oco logo abaixo.",
    "Você sente algo tocar seu tornozelo. Quando recua, vê apenas água escorrendo entre as pedras.",
    "Há uma marca de mão na parede. Os dedos são longos demais para pertencer a uma pessoa.",
    "Alguma coisa sussurra muito baixo atrás das pedras. Você não consegue distinguir palavras.",
    "O teto desaparece na escuridão por alguns metros antes de voltar a se fechar sobre o corredor.",
    "Um fio de água escorre pela parede. A água é limpa, mas deixa uma mancha avermelhada na pedra.",
    "Você passa por uma pilha de pedras cuidadosamente empilhadas. Há um osso pequeno no topo.",
    "O ar aqui tem gosto metálico. Sua língua formiga por alguns instantes.",
    "Uma sombra cruza o fim do corredor. Não há som de passos acompanhando-a.",
    "A rocha foi entalhada com dezenas de pequenos círculos. Todos possuem um ponto no centro, como olhos.",
    "Você escuta um soluço distante. Ele se repete exatamente igual alguns segundos depois.",
    "A passagem é larga, mas você sente a estranha necessidade de caminhar pelo centro dela.",
]

def descricao_ambiente_aleatoria():
    return random.choice(DESCRICOES_ALEATORIAS)


OBSERVACOES_ALEATORIAS = [
    "A passagem continua na penumbra. Você não percebe movimento imediato.",
    "O caminho parece livre, embora a escuridão esconda o que existe alguns passos adiante.",
    "Você distingue apenas pedra irregular e sombras. Nada se move, por enquanto.",
    "O corredor segue adiante. Um ruído distante ecoa e desaparece antes que você identifique a origem.",
    "A passagem está aberta. Há algo no cheiro do ar que faz você hesitar.",
    "Nada bloqueia o caminho, mas o silêncio adiante parece deliberado.",
    "A escuridão engole a passagem depois de poucos metros. Você não vê nada se aproximando.",
    "O caminho está livre. Pequenos fragmentos de pedra deslizam sozinhos pelo chão mais adiante.",
    "Você não vê obstáculo imediato. Ainda assim, alguma coisa faz seu estômago apertar.",
    "A passagem parece segura o bastante para atravessar. Isso, aqui embaixo, não significa muita coisa.",
]

DESCRICOES = {
    (1, 1): (
        "A entrada desaba atrás de você com um ruído seco. "
        "A escadaria pela qual desceu agora termina sob toneladas de rocha. "
        "O ar cheira a ferrugem, terra molhada e algo vagamente doce demais."
    ),
    (1, 3): (
        "Um nicho foi escavado na parede. Dentro dele repousa uma lâmina curta, "
        "coberta por uma crosta escura que você prefere acreditar ser ferrugem."
    ),
    (1, 11): (
        "O teto se abre numa câmara alta. Cordões de raízes descem da escuridão "
        "e se enrolam em um pedestal feito de vértebras calcificadas."
    ),
    (3, 1): (
        "Você encontra restos de um acampamento antigo. O tecido das mochilas "
        "virou pó, mas um frasco ainda está intacto entre costelas humanas."
    ),
    (3, 7): (
        "As paredes deixam de ser pedra talhada e tornam-se rocha natural. "
        "Algo riscou sulcos paralelos no chão, como se tivesse sido arrastado daqui repetidas vezes."
    ),
    (3, 9): (
        "Uma névoa esverdeada rasteja rente ao chão. Pequenos insetos jazem imóveis dentro dela, "
        "com as patas retorcidas contra o próprio corpo. Respirar aqui parece uma ideia ruim."
    ),
    (3, 10): (
        "Há marcas úmidas no chão. Elas começam pequenas e humanas, "
        "mas cada pegada seguinte possui dedos mais longos do que a anterior."
    ),
    (4, 9): (
        "Uma fenda negra corta o caminho. Lá embaixo não se ouve água, pedra ou vento. "
        "Apenas um som baixo e ritmado, parecido com respiração."
    ),
    (5, 5): (
        "Uma fileira de dentes humanos foi pressionada contra a argamassa da parede. "
        "Todos apontam para o mesmo corredor."
    ),
    (5, 7): (
        "Um cadáver ainda veste uma malha de ferro quase intacta. "
        "O corpo dentro dela parece ter sido espremido até caber em metade do próprio tamanho."
    ),
    (7, 1): (
        "No fundo de uma cisterna seca há uma chave negra. "
        "Dezenas de unhas quebradas permanecem cravadas nas pedras ao redor dela."
    ),
    (7, 6): (
        "Pedras desabadas comprimem a passagem. Entre elas, você enxerga pedaços de uma mão "
        "que ainda se contrai lentamente, embora o resto do corpo não esteja à vista."
    ),
    (9, 4): (
        "Um arco de pedra fecha o corredor. Runas cobrem sua superfície, "
        "mas não brilham: elas parecem fundos cortes que continuam sangrando."
    ),
    (9, 7): (
        "Símbolos azulados flutuam alguns centímetros acima da pedra, movendo-se como vermes sob vidro. "
        "Você sente pressão atrás dos olhos quando tenta focá-los."
    ),
    (9, 8): (
        "Uma espada repousa sobre um altar rachado. A lâmina está limpa demais para este lugar."
    ),
    (9, 10): (
        "Uma pequena chave translúcida flutua alguns centímetros acima do chão. "
        "Dentro dela, algo semelhante a uma pupila acompanha seus movimentos."
    ),
    (10, 13): (
        "Diante de você ergue-se o Portão do Corvo. Três fechaduras formam um triângulo "
        "no centro da porta. Do outro lado vem uma corrente de ar frio: a primeira prova "
        "de que o mundo exterior ainda existe."
    ),
    (11, 6): (
        "O corredor se alarga de forma antinatural. Ossos estão dispostos em círculos concêntricos. "
        "Alguma coisa enorme dorme entre eles, coberta por um manto feito de pele costurada."
    ),
    (11, 11): (
        "Uma poça de água perfeitamente imóvel reflete um teto que não existe. "
        "No reflexo, há alguém de pé atrás de você."
    ),
}

PREVISOES = {
    (1, 3): "Você distingue o brilho opaco de uma pequena lâmina dentro de um nicho.",
    (1, 11): "Há uma câmara aberta adiante e algo pendurado sobre um pedestal.",
    (3, 9): "Uma névoa esverdeada ocupa a passagem. O cheiro é acre e adocicado.",
    (3, 10): "Você vê pegadas molhadas desaparecendo na escuridão.",
    (4, 9): "O chão termina abruptamente. Há uma fenda larga no caminho.",
    (5, 7): "Há um corpo coberto por metal no chão.",
    (7, 1): "Você percebe o contorno de uma cisterna seca e algo escuro no fundo.",
    (7, 6): "A passagem parece bloqueada por um desabamento.",
    (9, 4): "Um arco coberto por inscrições impede o avanço.",
    (9, 7): "Símbolos luminosos se movem sobre a parede sem permanecer no mesmo lugar.",
    (9, 8): "Algo metálico repousa sobre uma superfície de pedra.",
    (9, 10): "Há um brilho vítreo suspenso no ar.",
    (10, 13): "Uma porta monumental possui três fechaduras.",
    (11, 6): (
        "Você sente um cheiro sufocante de sangue velho. "
        "Algo muito grande parece respirar adiante. Continuar seria uma escolha consciente."
    ),
}


ITENS_INICIAIS = {
    (1, 3): [
        {"nome": "Adaga Enferrujada", "tipo": "arma", "dado": (1, 6),
         "descricao": "Uma adaga curta. Dano: 1d6."}
    ],
    (1, 11): [
        {"nome": "Chave de Osso", "tipo": "chave",
         "descricao": "Uma das três chaves do Portão do Corvo."}
    ],
    (3, 1): [
        {"nome": "Poção de Vida", "tipo": "cura", "dado": (1, 6),
         "descricao": "Recupera 1d6 de Vida."}
    ],
    (5, 7): [
        {"nome": "Malha de Ferro", "tipo": "armadura", "reducao": 1,
         "descricao": "Reduz em 1 degrau o dado de dano físico recebido."}
    ],
    (7, 1): [
        {"nome": "Chave Negra", "tipo": "chave",
         "descricao": "Uma das três chaves do Portão do Corvo."}
    ],
    (8, 5): [
        {"nome": "Poção de Mana", "tipo": "mana", "dado": (1, 6),
         "descricao": "Recupera 1d6 de Mana."}
    ],
    (9, 8): [
        {"nome": "Espada do Altar", "tipo": "arma", "dado": (1, 8),
         "descricao": "Uma espada estranhamente intacta. Dano: 1d8."}
    ],
    (9, 10): [
        {"nome": "Chave Vítrea", "tipo": "chave",
         "descricao": "Uma das três chaves do Portão do Corvo."}
    ],
    (11, 6): [
        {"nome": "Escudo do Carcereiro", "tipo": "escudo", "reducao": 1,
         "descricao": "Reduz em mais 1 degrau o dado de dano físico recebido."}
    ],
}


INIMIGOS_INICIAIS = {
    (3, 10): {
        "nome": "Rastejante Pálido",
        "vida": 7,
        "dano": (1, 4),
        "terrivel": False,
        "descricao": (
            "Uma criatura do tamanho de uma criança sai de trás da rocha. "
            "Ela se move sobre quatro membros humanos, mas todos os joelhos dobram para o lado errado. "
            "A cabeça não possui olhos. Mesmo assim, ela olha diretamente para você."
        ),
        "pontos": 35,
    },
    (11, 6): {
        "nome": "Carcereiro sem Rosto",
        "vida": 24,
        "dano": (2, 8),
        "terrivel": True,
        "descricao": (
            "A massa sob o manto se ergue. É alta demais para permanecer reta no corredor. "
            "Onde deveria haver um rosto existe pele lisa costurada com fio preto. "
            "Quatro braços emergem de seu tórax e cada mão termina em dedos cobertos por pequenas bocas."
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


# Ordem dos degraus de dano.
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
    print("\n=== CRIAÇÃO DO PERSONAGEM ===")
    nome = input("Nome do aventureiro: ").strip() or "Sem Nome"

    atributos = {atributo: 1 for atributo in ATRIBUTOS}
    pontos = 5

    print("\nTodos os atributos começam em 1.")
    print("Distribua 5 pontos extras. Máximo inicial: 3.\n")

    while pontos > 0:
        mostrar_atributos(atributos)
        print(f"Pontos restantes: {pontos}")
        escolha = input("Atributo para aumentar: ").strip().lower()

        atributo_encontrado = None
        for atributo in ATRIBUTOS:
            if atributo.lower().startswith(escolha):
                atributo_encontrado = atributo
                break

        if atributo_encontrado is None:
            print("Atributo inválido.\n")
            continue

        if atributos[atributo_encontrado] >= 3:
            print("Esse atributo já está no máximo inicial.\n")
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
    arma = jogador["arma"]["nome"] if jogador["arma"] else "Improvisada (1d4)"
    armadura = jogador["armadura"]["nome"] if jogador["armadura"] else "Nenhuma"
    escudo = jogador["escudo"]["nome"] if jogador["escudo"] else "Nenhum"

    print("\n=== STATUS ===")
    print(f"Nome: {jogador['nome']}")
    print(f"Vida: {jogador['vida']}/{jogador['vida_max']}")
    print(f"Mana: {jogador['mana']}/{jogador['mana_max']}")
    print(f"Chaves: {jogador['chaves']}/3")
    print(f"Pontos: {jogador['pontos']}")
    mostrar_atributos(jogador["atributos"])
    print(f"Arma: {arma}")
    print(f"Armadura: {armadura}")
    print(f"Escudo: {escudo}")


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

    print(f"\n[{atributo.upper()}] Dificuldade: {dificuldade}")
    print(f"Rolagens ({quantidade}d20): {resultados}")
    print(f"Melhor resultado: {melhor}")

    if melhor >= dificuldade:
        print("SUCESSO.")
        return True

    print("FALHA.")
    return False


# ============================================================
# INVENTÁRIO E ITENS
# ============================================================

def listar_inventario(jogador):
    print("\n=== INVENTÁRIO ===")
    if not jogador["inventario"]:
        print("Seu inventário está vazio.")
        return

    for i, item in enumerate(jogador["inventario"], start=1):
        print(f"{i}. {item['nome']} - {item['descricao']}")


def pegar_itens(jogador, itens_no_mapa):
    pos = jogador["posicao"]
    itens = itens_no_mapa.get(pos, [])

    if not itens:
        print("Não há nada aqui que você consiga levar.")
        return

    while itens:
        item = itens.pop(0)
        jogador["inventario"].append(item)
        print(f"Você pegou: {item['nome']}.")

        if item["tipo"] == "chave":
            jogador["chaves"] += 1
            jogador["pontos"] += 100
            print(f"Chaves encontradas: {jogador['chaves']}/3.")

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
        print("Você não possui esse item.")
        return

    if item["tipo"] == "arma":
        jogador["arma"] = item
        print(f"Você equipou {item['nome']}. Dano agora: {texto_dado(item['dado'])}.")
    elif item["tipo"] == "armadura":
        jogador["armadura"] = item
        print(f"Você vestiu {item['nome']}.")
    elif item["tipo"] == "escudo":
        jogador["escudo"] = item
        print(f"Você equipou {item['nome']}.")
    else:
        print("Esse item não pode ser equipado.")


def usar_item(jogador, trecho_nome):
    item = encontrar_item(jogador, trecho_nome)

    if not item:
        print("Você não possui esse item.")
        return

    if item["tipo"] == "cura":
        quantidade, lados = item["dado"]
        cura = dano_total((quantidade, lados))
        antes = jogador["vida"]
        jogador["vida"] = min(jogador["vida_max"], jogador["vida"] + cura)
        jogador["inventario"].remove(item)
        print(f"Você recuperou {jogador['vida'] - antes} de Vida.")
    elif item["tipo"] == "mana":
        quantidade, lados = item["dado"]
        cura = dano_total((quantidade, lados))
        antes = jogador["mana"]
        jogador["mana"] = min(jogador["mana_max"], jogador["mana"] + cura)
        jogador["inventario"].remove(item)
        print(f"Você recuperou {jogador['mana'] - antes} de Mana.")
    else:
        print("Esse item não é consumível.")


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
        print("Direção inválida. Use norte, sul, leste ou oeste.")
        return

    linha, coluna = destino
    if not dentro_do_mapa(linha, coluna):
        print("Não há caminho nessa direção.")
        return

    if MAPA_BASE[linha][coluna] == "#":
        paredes_conhecidas.add((linha, coluna))
        print("Há apenas pedra diante de você. Nenhuma passagem.")
        return

    print("\nVocê permanece onde está e observa com cuidado...")

    if destino in PREVISOES:
        print(PREVISOES[destino])
    else:
        simbolo = MAPA_BASE[linha][coluna]
        if simbolo == "B":
            print("A passagem está tomada por pedras pesadas.")
        elif simbolo == "F":
            print("O caminho parece interrompido por uma fenda.")
        elif simbolo == "R":
            print("Você distingue inscrições antigas numa estrutura de pedra.")
        elif simbolo == "V":
            print("Uma névoa insalubre ocupa o caminho. Seu corpo reage antes mesmo de você entrar.")
        elif simbolo == "A":
            print("Há símbolos arcanos adiante. Eles parecem mudar quando você tenta focalizá-los.")
        elif simbolo == "G":
            print("Uma construção monumental bloqueia o caminho.")
        else:
            print(random.choice(OBSERVACOES_ALEATORIAS))

    if destino in inimigos and inimigos[destino]["vida"] > 0:
        inimigo = inimigos[destino]
        if inimigo["terrivel"]:
            print("E há algo vivo ali. Grande demais. Você ainda pode escolher não entrar.")
        else:
            print("Você percebe movimento adiante.")


def descrever_local(jogador, itens_no_mapa, inimigos):
    pos = jogador["posicao"]
    print("\n" + "=" * 60)
    if pos in DESCRICOES:
        print(DESCRICOES[pos])
    else:
        print(descricao_ambiente_aleatoria())

    if pos in itens_no_mapa and itens_no_mapa[pos]:
        nomes = ", ".join(item["nome"] for item in itens_no_mapa[pos])
        print(f"\nVocê percebe algo que pode ser recolhido: {nomes}.")

    if pos in inimigos and inimigos[pos]["vida"] > 0:
        print("\nHá uma criatura aqui.")


def tentar_obstaculo(jogador, simbolo, obstaculos_resolvidos, destino):
    if destino in obstaculos_resolvidos:
        return True

    if simbolo == "B":
        print("\nUm desabamento bloqueia a passagem.")
        print("[FORÇA] Abrir espaço entre as pedras.")
        if teste_atributo(jogador, "Força", 11):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 20
            print("Você força as pedras até abrir uma passagem estreita.")
            return True

        dano = rolar_dado(4)
        jogador["vida"] -= dano
        print(f"Uma pedra despenca sobre seu ombro. Você perde {dano} de Vida.")
        return False

    if simbolo == "F":
        print("\nUma fenda larga corta o caminho.")
        print("[AGILIDADE] Saltar para o outro lado.")
        if teste_atributo(jogador, "Agilidade", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 20
            print("Você salta e alcança a margem oposta.")
            return True

        dano = rolar_dado(6)
        jogador["vida"] -= dano
        print(
            f"Você escorrega, bate contra a rocha e consegue se puxar de volta. "
            f"Perde {dano} de Vida."
        )
        return False

    if simbolo == "R":
        print("\nAs runas fecham a passagem como uma ferida cicatrizada.")
        print("Este mecanismo exige raciocínio; força bruta não encontra onde agir.")
        if teste_atributo(jogador, "Intelecto", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 25
            print("Você identifica a sequência correta. A pedra se abre com um gemido.")
            return True

        dano = rolar_dado(4)
        jogador["mana"] = max(0, jogador["mana"] - dano)
        print(f"As runas reagem à tentativa. Você perde {dano} de Mana.")
        return False

    if simbolo == "V":
        print("\nUma névoa venenosa preenche o corredor.")
        print("[VIGOR] Prender a respiração e atravessar antes que o veneno paralise seus músculos.")
        if teste_atributo(jogador, "Vigor", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 25
            print(
                "Sua garganta queima e seus olhos lacrimejam, mas seu corpo resiste. "
                "Você atravessa antes que a névoa consiga dominá-lo."
            )
            return True

        dano = rolar_dado(6)
        jogador["vida"] -= dano
        print(
            f"Seus músculos endurecem de repente. Você cai de joelhos e só consegue "
            f"se arrastar de volta quando o efeito começa a ceder. Perde {dano} de Vida."
        )
        return False

    if simbolo == "A":
        print("\nSímbolos arcanos se movem sobre a pedra como organismos vivos.")
        print("[ARCANA] Estudar o padrão mágico e deduzir como atravessar sem ativá-lo.")
        if teste_atributo(jogador, "Arcana", 12):
            obstaculos_resolvidos.add(destino)
            jogador["pontos"] += 30
            print(
                "Você percebe que as runas não formam palavras, mas uma sequência de pulsos mágicos. "
                "Ao sincronizar seus passos com o padrão, a pressão no ar desaparece."
            )
            return True

        perda_mana = rolar_dado(6)
        dano = rolar_dado(4)
        jogador["mana"] = max(0, jogador["mana"] - perda_mana)
        jogador["vida"] -= dano
        print(
            f"Você interpreta o fluxo de forma errada. A magia atravessa seus pensamentos como uma lâmina. "
            f"Perde {perda_mana} de Mana e {dano} de Vida."
        )
        return False

    return True


# ============================================================
# COMBATE
# ============================================================

def combate(jogador, inimigo):
    print("\n" + "!" * 60)
    print(inimigo["descricao"])
    print(f"\nINIMIGO: {inimigo['nome']}")
    print(f"Vida: {inimigo['vida']} | Dano: {texto_dado(inimigo['dano'])}")

    if inimigo["terrivel"]:
        print(
            "\nIsto não parece uma luta justa. Criaturas terríveis são feitas para "
            "ser enfrentadas com bom equipamento. Fugir continua sendo uma opção."
        )

    while inimigo["vida"] > 0 and jogador["vida"] > 0:
        print(
            f"\nSua Vida: {jogador['vida']}/{jogador['vida_max']} | "
            f"Mana: {jogador['mana']}/{jogador['mana_max']}"
        )
        print("Ações: atacar | magia | fugir | usar <item>")
        acao = input("> ").strip().lower()

        if acao == "atacar":
            dado = dado_arma(jogador)
            dano = dano_total(dado)
            inimigo["vida"] -= dano
            print(f"Você ataca com {texto_dado(dado)} e causa {dano} de dano.")

        elif acao == "magia":
            custo = 3
            if jogador["mana"] < custo:
                print("Mana insuficiente.")
                continue
            jogador["mana"] -= custo
            dano = dano_total((1, 8))
            inimigo["vida"] -= dano
            print(f"A descarga arcana causa {dano} de dano. (-{custo} Mana)")

        elif acao.startswith("usar "):
            usar_item(jogador, acao[5:].strip())
            continue

        elif acao == "fugir":
            custo = rolar_dado(4)
            jogador["vida"] = max(1, jogador["vida"] - custo)
            print(
                f"Você recua em pânico e se fere na fuga. Perde {custo} de Vida, "
                "mas permanece vivo."
            )
            return "fugiu"

        else:
            print("Ação inválida.")
            continue

        if inimigo["vida"] <= 0:
            print(f"\n{inimigo['nome']} cai. Por alguns segundos, ainda tenta respirar.")
            jogador["pontos"] += inimigo["pontos"]
            return "venceu"

        # Turno do inimigo
        reducoes = reducao_defesa(jogador)
        dado_reduzido = reduzir_dado(inimigo["dano"], reducoes)

        if dado_reduzido == (0, 0):
            print(
                f"{inimigo['nome']} ataca, mas sua proteção absorve completamente o golpe."
            )
        else:
            dano = dano_total(dado_reduzido)
            jogador["vida"] -= dano
            print(
                f"{inimigo['nome']} ataca. Sua defesa reduz "
                f"{texto_dado(inimigo['dano'])} para {texto_dado(dado_reduzido)}. "
                f"Você sofre {dano} de dano."
            )

    return "morto"


# ============================================================
# MAPA DESCOBERTO
# ============================================================

def mostrar_mapa_descoberto(jogador, visitados, paredes_conhecidas):
    print("\n=== MAPA EXPLORADO ===")
    print("@ = você | · = local visitado | ■ = parede conhecida | ? = desconhecido")

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
        print("Ainda não há pontuações salvas.")
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
        print("Ainda não há pontuações válidas.")
        return

    for posicao, (nome, pontos, resultado) in enumerate(registros[:10], start=1):
        print(f"{posicao:>2}. {nome:<20} {pontos:>4} pts  ({resultado})")


# ============================================================
# JOGO PRINCIPAL
# ============================================================

def ajuda():
    print("""
=== COMANDOS ===
n / norte              mover para o norte
s / sul                mover para o sul
l / leste              mover para o leste
o / oeste              mover para o oeste

olhar norte             observar antes de entrar
olhar sul
olhar leste
olhar oeste

examinar                repetir/observar melhor o local atual
pegar                   pegar os itens do local
inventario              mostrar seus itens
equipar <item>          equipar arma, armadura ou escudo
usar <item>             usar poção
status                  mostrar ficha
mapa                    mostrar somente áreas já exploradas
ajuda                   mostrar esta lista
sair                    abandonar a partida
""")


def jogar():
    jogador = criar_personagem()
    itens_no_mapa = deepcopy(ITENS_INICIAIS)
    inimigos = deepcopy(INIMIGOS_INICIAIS)
    obstaculos_resolvidos = set()
    visitados = {POSICAO_INICIAL}
    paredes_conhecidas = set()

    print("\n" + "=" * 60)
    print("THE DUNGEONEER")
    print("=" * 60)
    print(
        "Você acorda sob Myrthwa, em algum ponto entre o calabouço dos antigos reis "
        "e as cavernas que existiam muito antes deles.\n"
        "Dizem que três chaves abrem o único portão para a superfície.\n"
        "Dizem também que ninguém que encontrou as três voltou para confirmar."
    )

    descrever_local(jogador, itens_no_mapa, inimigos)
    ajuda()

    while jogador["vida"] > 0:
        comando = input("\n> ").strip().lower()

        if not comando:
            continue

        if comando in DIRECOES:
            destino = posicao_na_direcao(jogador["posicao"], comando)
            linha, coluna = destino

            if not dentro_do_mapa(linha, coluna):
                print("Não há caminho nessa direção.")
                continue

            if MAPA_BASE[linha][coluna] == "#":
                paredes_conhecidas.add((linha, coluna))
                print("A pedra bloqueia completamente esse caminho.")
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
                        f"O Portão do Corvo possui três fechaduras. "
                        f"Você carrega apenas {jogador['chaves']} chave(s)."
                    )
                    continue

                jogador["posicao"] = destino
                visitados.add(destino)
                descrever_local(jogador, itens_no_mapa, inimigos)
                jogador["pontos"] += 250
                print(
                    "\nAs três chaves giram ao mesmo tempo.\n"
                    "O portão se abre e, pela primeira vez em horas, você sente vento verdadeiro.\n"
                    "Atrás de você, alguma coisa começa a correr pelos corredores.\n"
                    "Você não olha para trás.\n\n"
                    "VOCÊ ESCAPOU DO CALABOUÇO."
                )
                salvar_pontuacao(jogador, "ESCAPOU")
                print(f"Pontuação final: {jogador['pontos']}")
                return

            posicao_anterior = jogador["posicao"]
            jogador["posicao"] = destino
            visitados.add(destino)
            descrever_local(jogador, itens_no_mapa, inimigos)

            # Combate ao entrar em um local ocupado.
            if destino in inimigos and inimigos[destino]["vida"] > 0:
                resultado = combate(jogador, inimigos[destino])

                if resultado == "fugiu":
                    jogador["posicao"] = posicao_anterior
                    print("Você retorna para a passagem anterior.")
                elif resultado == "morto":
                    break

        elif comando.startswith("olhar "):
            direcao = comando[6:].strip()
            observar_direcao(jogador, direcao, inimigos, paredes_conhecidas)

        elif comando == "examinar":
            descrever_local(jogador, itens_no_mapa, inimigos)

        elif comando in ("pegar", "pegar item", "pegar itens"):
            pegar_itens(jogador, itens_no_mapa)

        elif comando == "inventario":
            listar_inventario(jogador)

        elif comando.startswith("equipar "):
            equipar_item(jogador, comando[8:].strip())

        elif comando.startswith("usar "):
            usar_item(jogador, comando[5:].strip())

        elif comando == "status":
            mostrar_status(jogador)

        elif comando == "mapa":
            mostrar_mapa_descoberto(jogador, visitados, paredes_conhecidas)

        elif comando == "ajuda":
            ajuda()

        elif comando == "sair":
            print("Você abandona a expedição.")
            salvar_pontuacao(jogador, "ABANDONOU")
            return

        else:
            print("Comando desconhecido. Digite 'ajuda' para ver os comandos.")

    print(
        "\nSuas pernas cedem. A última coisa que você ouve é algo se aproximando "
        "devagar, como se soubesse que já não há motivo para correr."
    )
    print("\nVOCÊ MORREU.")
    salvar_pontuacao(jogador, "MORREU")
    print(f"Pontuação final: {jogador['pontos']}")


def menu():
    while True:
        print("\n" + "=" * 60)
        print("THE DUNGEONEER - PROTÓTIPO")
        print("=" * 60)
        print("1. Jogar")
        print("2. Ver ranking")
        print("3. Sair")

        escolha = input("> ").strip()

        if escolha == "1":
            jogar()
        elif escolha == "2":
            mostrar_ranking()
        elif escolha == "3":
            print("Até a próxima.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
