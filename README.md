# Empire_Car_Racing_Game

## Overview Of The Game
This Car Racing Game is a simple 2D, yet engaging driving game built using the pygame library. 

The player controls a car and navigates through a series of lanes while avoiding enemy vehicles and trying to complete each level within a set time limit.

The game features multiple levels, scoring, and a dynamic game environment with increasing speed and difficulty as the player progresses.

The game also implements pygame mixer to which implements a background music that runs on a loop as a user plays the game and enhances enjoyment while playing it. It maximises the user experience

## Features Of The Game

 * **Player Control:** The player controls a car that can move left and right across different lanes.
 * **Enemy Vehicles:** Enemy vehicles appear randomly on the road, and the player must avoid colliding with them.
 * **Lane System:** The game features a multi-lane road, with lane markers that move continuously to simulate forward motion.
 * **Scoring System:** The player's score increases as they successfully avoid enemy vehicles and keep playing.
 * **Game Over Conditions:** The game ends if the player's car collides with an enemy vehicle or if the time limit for the level is reached.
 * **Multiple Levels:** The game includes several levels with increasing difficulty and faster speeds.
 * **Time Limit:** Each level has a time limit that the player must beat to progress.
 * **Pause Functionality:** The game can be paused by pressing the spacebar.
 * **Game Over and Restart:** Upon a game over, the player has options to restart, advance to the next level, or quit.
  
## Game Controls
 * **Left Arrow Key (←):** Move the car to the left lane.
 * **Right Arrow Key (→):** Move the car to the right lane.
 * **Spacebar:** Pause or unpause the game.
 * **Y:** Restart the game or a level.
 * **N:** Proceed to the next level.
 * **Q or ESC:** Quit the game.
  


## Game Setup and Requirements



 ## The Game Flow

  * **Level Selection:** At the start of the game, the player will be prompted to choose a level. 
     * Each level has its own difficulty and vehicle   limit.
  
  * **Gameplay:** The player navigates through the lanes and avoids colliding with enemy vehicles.
  * **Game Over:** If the player collides with an enemy vehicle or runs out of time, the game ends, and the player can choose to restart or proceed
  * **Score and Timer:** The score and remaining time are displayed on the screen. The player gains points by successfully avoiding vehicles and completing levels.
  * **Next Level:** If the player completes a level, they are given the option to advance to the next level.
  
 ### The Game Logic and Structure

 * **Game Loop:** The game runs inside a continuous loop that checks for player input, updates the game state, and redraws the screen.
 * **Collision Detection:** The game checks for collisions between the player's car and enemy vehicles. If a collision occurs, the game ends.
 * **Enemy Vehicles:** Enemy vehicles are randomly generated within the available lanes. They move downward on the screen, and the player must avoid them.
  
 * **Level Progression:** As the player progresses through levels, the game speed increases, and the number of enemy vehicles also grows.
 * **Pause Functionality:** The game can be paused by pressing the spacebar, allowing the player to take a break.



### Prerequisites

Before running the game, you will need to install Python and the pygame library.

 1. **VsCode** Install to view the codes

 2. **git clone** ````git clone <SSH KEY>```` the repository to your local machine in the terminal

 3. **Python:** You can download Python from [python.org](https://www.python.org/downloads/) or you can install it in your terminal.

 4. **pygame Library:** You can install pygame using pip: ``pip install pygame``
   
 5. **Running the Game:**  Once you have Python and pygame installed, you can start the game by running the script. Using the following command  in your terminal or command prompt: ``python3 main.py``
   

### Acknowledgements
This game was built using the pygame library. All fonts and game assets are created specifically for this game.

The Images were Sourced from the previously done projects in Youtube, Reddit, Github and StackOverflow.
The images are transparent to make them not be with  a  background color

### Contributing
Feel free to fork this repository and contribute improvements! 


### Author

* Elly James    <ellykomunga@gmail.com>

Incase you are stuck or experiencing any error, reach out to us via our respective emails

### License
This game is open-source and licensed under the MIT License.

Have fun playing, and remember to avoid those cars on the road! 🏎💨













