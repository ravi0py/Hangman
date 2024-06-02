# Hangman Game

The Hangman game is a classic word-guessing game where the player tries to guess a secret word by suggesting letters. The game provides a set of hangman pictures to indicate the number of incorrect guesses made by the player.

## Features

- **Multiple Levels**: The game offers three levels of difficulty: Easy, Moderate, and Hard.
- **Random Word Selection**: The game selects a random word from a predefined list for each level.
- **Scorekeeping**: The game keeps track of the player's score and saves it to a database.
- **Hall of Fame**: The game displays the top scores for each level in the Hall of Fame.

## How to Play

1. **Enter Your Name**: Enter your name to start the game.
2. **Choose a Level**: Select a level of difficulty: Easy, Moderate, or Hard.
3. **Choose a Category**: Select a category: Animals, Shapes, or Places.
4. **Guess Letters**: Guess letters to try to reveal the secret word.
5. **Save Your Score**: The game saves your score to the database after each game.

## Requirements

- Python 3.8+: The game requires Python 3.8 or later to run.
- `sqlite3`: The game uses the `sqlite3` library to manage the database.

## Installation

1. **Clone the Repository**: Clone the repository using:
   ```sh
   git clone git@github.com:ravi0py/Hangman.git
