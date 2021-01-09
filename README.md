# Decision-Tree-Game

## Introduction
Dyslexia is a common learning difficulty that can cause problems with reading, writing and spelling.
It's a specific learning difficulty, which means it causes problems with certain abilities used for learning, such as reading and writing.
## Project main goal
The main idea of this project is creating a simple game for children between 3 to 8 years old that can identify dyslexia. In order to prevent it's develop over the age. The game is not only a 'match the correct word', it also introduce a bit of data analysis and can recognise patrons between all the players over the time. It generate a excel that everyteacher can complement with the behaviour notes of the children.
## Tecnology used:
### MQTT:
Every children is connected to the teacher's topic in order to receive the number of words and the game mode.
The teacher is continously listenning all the childrens in order to make the ranking of the most fail words.
An ESP32 is also connected to the listen topic of the children console, in every state machine of the children the embeded device is going to change the color of their leds ir order to indicate the status of the game.
### Pygame
All the GUI is implemented using pygame and the data and color informations is introduce via a json file filled by a real teacher that can change over the diferent classes or acording the children evolution.

For simple execution there is a .bat file that can easily run the program and simulate multiple children.
## Images of the real game:
### Waiting other children: ###
<img src="https://github.com/RarceD/Decision-Tree-Game/tree/main/Documentation/images_readme/waiting_other_children.png" alt="drawing" width="300"/>

### On game ###
<img src="https://github.com/RarceD/Decision-Tree-Game/blob/main/Documentation/images_readme/waiting_other_children.png" alt="drawing" width="300"/>

