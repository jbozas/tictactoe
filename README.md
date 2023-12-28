# TicTacToe API - Local Deployment

This guide provides instructions for deploying the TicTacToe API locally using Docker.

## Instructions

1. **Build Docker Image:**
   ```bash
   docker build -t tictac .
   ```

2. **Run Docker Container:**
   ```bash
   docker run -p 8000:8000 tictac
   ```

## Improvements Ideas

### Create a Game
* Allow players to choose their symbols with the optional parameter "symbol" during game creation.
* Enable players to determine the starting player by providing the optional parameter "starting_player." If not specified, the first player in the list plays first.
* Implement robust input validation and handling of malformed inputs or invalid data using serializers.

### Make a Play
* Enhance input validation for malformed inputs or invalid data. Address scenarios like a player attempting two consecutive moves or making a move in a finished game.
* Leverage serializer and board logic to handle these scenarios and ensure valid gameplay.

### List All Games
* Extend the endpoint to filter and return only finished or unfinished games using optional QueryParams.
* Implement pagination to handle scenarios where millions of games are stored, avoiding the need to return all games at once.

### Retrieve a Single Game
* Handle cases where the ID is invalid by incorporating logic within the serializer.
* Address scenarios where the data needed for listing games differs from that required for retrieving a single game. Implement separate serializers for these cases.

### Delete a Game
* Manage cases where the ID is invalid through serializer logic.
* Prevent attempts to delete an already deleted game by using a service that raises an error if a game cannot be deleted.

## Areas for Further Improvement

* Implement a empate-handling mechanism.
* Introduce pagination for the list of games.
* Enhance test coverage to ensure comprehensive unit testing.
* Implement better handling of players with repeated names.
