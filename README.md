**Status:** Early Development 

This is a module that provides a gym style API for the turnbased strategy game Prismata.

Requires the 'prismataengine' module, which is a Python3 wrapper for the C++ code developed and published by David Churchill/Lunarch Studios [...]

- Currently only baseset and a 4 card "steelsplitter only" games are available (WIP)
- State and action serialization take advantage of permutation symmetry; can use one-hot encodings or raw values of numbers of cards.
- 2-Player game. Currently 'Active Player' is just part of the state output.
- Set up to train against specified policies from the engine or a neural network opponent for self-play purposes
- More documentation to come; please see smkravec/prismata-rl for a working example of an RL pipeline

Info about Prismata:
- 2 Player
- Perfect information
- Deterministic
- Random units at initialization with very different abilities
- Complicated action space, large and dynamic even within a game

# Installation

From source:
```bash
git clone smkravec/gym-prismata
cd gym-prismata
pip install .
```
