**Status:** Early Development 

Requires the 'prismataengine' module, which is a Python3 wrapper for the C++ code developed and published by David Churchill/Lunarch Studios [...]

Prismata engine unlikely to change in a way that breaks everything, but possible
Currently only baseset confidently supported, but random units should be possible
Methods for the state and action space expected to change
Representation for state and action space not ideal; dimension of the action space dynamic.
2-Player game. Currently 'Active Player' is just part of the state output.
Currently only extremely sparse rewards (Victory/No Victory); will be updated

Info about Prismata:
2 Player
Perfect information
Deterministic
Random units at initialization with very different abilities
Complicated action space, large and dynamic even within a game

# Installation

```bash
pip install gym_prismata
```
