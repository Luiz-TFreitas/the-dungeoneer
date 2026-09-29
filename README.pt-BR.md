# The Dungeoneer

**Português** | [English](README.md)

**The Dungeoneer** é um RPG textual de fantasia sombria desenvolvido em Python.

O jogador explora um calabouço labiríntico fixo onde antigas construções subterrâneas se misturam com um enorme sistema de cavernas naturais. Para escapar, será necessário superar perigos ambientais, resolver puzzles, encontrar equipamentos, sobreviver às criaturas, recuperar **três chaves** e alcançar o portão final.

O projeto foi criado originalmente para a disciplina de **Algoritmos e Estruturas de Dados I**.

## Estado atual

**Protótipo / Desenvolvimento inicial**

Os principais sistemas do jogo já estão funcionais, enquanto o mapa, história, inimigos, itens, puzzles, balanceamento e outras mecânicas continuam sendo expandidos.

## Principais funcionalidades

- Calabouço representado por matriz
- Movimentação por Norte, Sul, Leste e Oeste
- Possibilidade de observar uma direção antes de entrar
- Mapa parcialmente revelado
- Seis atributos:
  - Força
  - Agilidade
  - Vigor
  - Arcana
  - Intelecto
  - Presença
- Testes de atributo utilizando múltiplos d20
- Sistemas de Vida e Mana
- Inventário e equipamentos
- Combate baseado em dados
- Armas, armaduras e escudos que modificam dados de dano
- **Flagelos**, criaturas raras e extremamente perigosas
- Puzzles e perigos ambientais
- Descrições atmosféricas aleatórias
- Três chaves necessárias para escapar
- Pontuação e ranking salvos em arquivo texto

## Exploração baseada em matriz

O calabouço é representado através de uma matriz bidimensional utilizando listas aninhadas do Python.

Cada posição pode representar paredes, espaços transitáveis, obstáculos, inimigos, itens, chaves, eventos ou a saída.

A posição do jogador é armazenada através de coordenadas:

```python
(linha, coluna)
```

A movimentação altera essas coordenadas, fazendo da matriz uma parte central da navegação, detecção de paredes, exploração e progressão.

## Testes de atributo

O valor de um atributo determina quantos dados de vinte lados são rolados.

Exemplo:

```text
Força: 3

Rolagens:
7, 16, 11

Resultado:
16
```

O maior resultado é utilizado.

Diferentes desafios podem exigir diferentes atributos, fazendo com que o jogador precise depender de mais de uma especialização.

## Combate

O combate ocorre propositalmente com pouca frequência.

A maioria das criaturas é relativamente fraca, porém o calabouço também abriga **Flagelos**: inimigos raros e excepcionalmente perigosos que podem exigir equipamentos melhores, preparação ou fuga.

Armas e criaturas utilizam dados para calcular dano, enquanto armaduras e escudos reduzem a força dos dados de dano recebidos.

## Ambientação

O jogo possui uma atmosfera de fantasia sombria com fortes elementos de terror.

Áreas comuns utilizam pequenas descrições aleatórias para tornar a exploração menos repetitiva, enquanto salas importantes, inimigos, puzzles e eventos possuem descrições próprias.

## Objetivo

Encontrar as **três chaves** e utilizá-las para abrir o portão final.

## Como executar

É necessário possuir Python 3 instalado.

```bash
cd the-dungeoneer
python PT_the_dungeoneer.py
```

Atualmente, nenhuma biblioteca externa é necessária.

## Idiomas

O projeto pretende possuir suporte a:

- Português brasileiro
- Inglês

O protótipo atual está sendo desenvolvido principalmente em português.

## Contexto acadêmico

O projeto foi criado para um trabalho que exige o desenvolvimento de um jogo utilizando uma **matriz** de forma significativa.

Em The Dungeoneer, a matriz é utilizada para representar o mapa, movimentação, paredes, obstáculos, eventos, inimigos, itens, exploração e saída.

## Desenvolvimento planejado

Entre as próximas adições estão:

- Ampliação do calabouço
- Mais puzzles e eventos narrativos
- Encontros utilizando Presença
- Mais equipamentos e inimigos
- Novos Flagelos
- Expansão do sistema de magia
- Melhor balanceamento
- Localização completa em português e inglês
- Separação do código em diferentes módulos

## Licença

Nenhuma licença foi definida até o momento.