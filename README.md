# The Dungeoneer

[Português](README.pt-BR.md) | **English**

**The Dungeoneer** is a text-based dark fantasy RPG developed in Python.

The player explores a fixed labyrinthine dungeon where ancient ruins merge with a vast underground cave system. To escape, the player must overcome environmental hazards, solve puzzles, find useful equipment, survive hostile creatures, recover **three keys**, and reach the final gate.

The project was originally created for an **Algorithms and Data Structures I** course.

## Current Status

**Prototype / Early Development**

The core gameplay systems are functional, while the map, story, enemies, items, puzzles, balancing, and other mechanics are still being expanded.

## Main Features

- Matrix-based dungeon map
- Movement using North, South, East, and West
- Ability to inspect nearby areas before entering them
- Partially revealed exploration map
- Six character attributes:
  - Strength
  - Agility
  - Vigor
  - Arcana
  - Intellect
  - Presence
- Attribute checks using multiple d20 rolls
- Health and Mana systems
- Inventory and equipment
- Dice-based combat
- Weapons, armor, and shields that modify damage dice
- Rare but dangerous **Scourges**
- Environmental puzzles and hazards
- Randomized atmospheric descriptions
- Three keys required to escape
- Score and ranking saved to a text file

## Matrix-Based Exploration

The dungeon is represented using a two-dimensional matrix built from nested Python lists.

Each position can represent walls, walkable areas, obstacles, enemies, items, keys, events, or the exit.

The player's position is stored using coordinates:

```python
(row, column)
```

Movement changes these coordinates, making the matrix a central part of navigation, collision detection, exploration, and progression.

## Attribute Checks

The value of an attribute determines how many d20s are rolled.

For example:

```text
Strength: 3

Rolls:
7, 16, 11

Result:
16
```

The highest roll is used.

Different challenges may require different attributes, encouraging the player to rely on more than a single specialization.

## Combat

Combat is intentionally uncommon.

Most creatures are relatively weak, but the dungeon also contains **Scourges**: rare and exceptionally dangerous enemies that may require better equipment, preparation, or retreat.

Weapons and creatures use dice for damage, while armor and shields reduce the strength of incoming damage dice.

## Atmosphere

The game uses a dark fantasy setting with strong horror elements.

Ordinary areas use short randomized descriptions to keep exploration varied, while important rooms, enemies, puzzles, and events have unique descriptions.

## Objective

Find all **three keys** and use them to unlock the final gate.

## Running the Game

Python 3 is required.

```bash
cd the-dungeoneer
python the_dungeoneer.py
```

No external Python packages are currently required.

## Languages

The project is planned to support:

- Brazilian Portuguese
- English

The current prototype is primarily being developed in Portuguese.

## Academic Context

The project was created for an assignment requiring the development of a game that meaningfully uses a **matrix**.

In The Dungeoneer, the matrix is used for the dungeon layout, player movement, walls, obstacles, events, enemies, items, exploration, and the exit.

## Planned Development

Future development includes:

- Expanded dungeon
- More puzzles and narrative events
- Presence-based encounters
- More equipment and enemies
- Additional Scourges
- Expanded magic system
- Improved balancing
- Full Portuguese and English localization
- Code organization into multiple modules

## License

No license has currently been selected.