# Overview

A game where there's you, a torch, and a dark maze. It's got wildly unique game mechanics such as top-down WASD or arrow key movement, random map generation, and an unprecedented dynamic lighting system will awe even RTX3090 owners. 

In other words: WASD or arrow keys to move around a grid, Q to quit, and the goal is to find the exit. 

Honestly, there isn't much to say about why I wanted to write it other than that I wanted to try making a game. The code and comments are a bit of a mess because it's a work-in-progress kind of thing that's definitely not what I'd consider finished; there's so much more I'd like to do with it still, and I've been having a lot of fun with it despite how simple it is. It's all very low-level stuff (I mean, it *is* just python at the end of the day), so it's not like I'm learning incredible game dev skills, but I wanted to make it, and so I did.

[Software Demo Video 1](https://youtu.be/E996ar84e1Y)

# Development Environment

Developed using Visual Studio Code

Languages used: Python: Arcade Library

# Useful Websites

I'll say it right here: Arcade Academy tutorials and documentation are your friend. There's way more there that I undoubtedly should have explored, but I wanted to just try building and adapting the stuff I saw right away, so there's probably way better ways to do everything I've done.
* [Arcade Academy](https://api.arcade.academy/en/latest/index.html)
* [RealPython Arcade Tutorial Program](https://realpython.com/arcade-python-game-framework/)
* [Itch.io](https://itch.io/)
* [Random Maze Generator by ChickenSlayer3000](https://github.com/ChickenSlayer3000/Random-Maze-Generator/blob/master/maze2.py)
* [Pixilart.com](https://www.pixilart.com/draw?ref=home-page)

# Future Work

This is just a pile of ideas that I'd like to fix and/or add to improve the game in various capacities.

* Fix player sprite hitbox to allow full-square steps instead of requiring half-squares to avoid shunting through walls.
* Go over the random maze generation and integrate it more optimally into my own structure (or do a better search for tutorials to make my own from scratch) and then modifying it with new options, such as throughputs, holes, or the end tile at the end of corridors. There is a low-chance crash error that occurs using the current method, so a ground-up redesign would also help.
* Get a creature that tries to chase you around the maze
* Dynamic maze lightning done better: Displaying walls and having variable transparency based on distance.
* Add the ability to drop torches behind you that emit light.
* Try to improve efficiency of sprite lists to make larger mazes viable; make sure I'm not calling update on literally everything in every circumstance.
* Add/make my own nicer spritework (including creating higher base sprite sizes so upscaling doesn't look bad)
* Flashlight mode: directional dynamic lighting and player-facing direction.