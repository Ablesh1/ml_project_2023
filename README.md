# machine_learning_project_2023

## 2048 implementation v 1.0.0

### Authors:
- [@Krzychu-Z](https://github.com/Krzychu-Z)

## Setup instruction
- [x] Download this repository
- [x] Run client_2048.py
- [x] Enjoy custom 2048 by launching 2048_index.html ;)

## Biomes edition (current)
Background image changes for each top value in the game.
Discover the beauty of the World while merging power-of-2 blocks.

### Sample levels:
#### Tundra (4)
![example image](img/biomes_1.png)

#### Oceanic climate (32)
![example image](img/biomes_2.png)

#### Humid subtropical climate (128)
![example image](img/biomes_3.png)

## Minimal edition
Plain game UI based on green gradient that contrasts perfectly with golden tiles.

### Sample levels:
#### Initial board (0)
![example image](img/minimal_2.jpg)

#### 4 level
![example image](img/minimal_3.jpg)

#### 32 level
![example image](img/minimal_4.jpg)

#### 256 level
![example image](img/minimal_5.jpg)

#### 1024 level
![example image](img/minimal_1.jpg)

## Technical documentation
Game works using websockets defined in Python websockets module.\
Websocket receives game board that is 2D array of ints and performs one swipe.\
Websocket from backend of this game can easily be used in ML purposes, since it works on standard 2D arrays.

More details can be found inside the code.

Websocket address: ws://localhost:8765

## Known bugs:
- Game incorrectly assumes losing scenario
![obraz](https://user-images.githubusercontent.com/47274258/232328581-59002010-d76d-4419-ac0a-3a27a53927a5.png)
