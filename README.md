

# Improvements ideas
## Create a Game
* How would you let the players choose their symbols instead of using X and O? There is an optional param "symbol" when creating a game.
* Let the players choose who goes first instead of always choosing the first player in the list? There is an optional param starting_player, if you dont send it, the first player on the list will be the first to play.
* How can the API validate and handle malformed inputs or invalid data? With Serializers I do all that job.
## Make a play
* How can the API validate and handle malformed inputs or invalid data? Consider
the case where the same player tries to play twice in a row, or a player attempts
to make a move to a finished game. All that logic is handled by the Serializer and returned when is_valid() is called. Also the board itself checks that before making a new movement.
## List all games
* How would you extend the endpoint to return only finished or unfinished games? There is an optional QueryParam to filter those types of Games.
* What would happen if you had millions of stored games? Is there something you
can do to avoid returning all of them at once? Pagination could be implemented.
## Retrieve a single game
* How would you handle the case where the ID is invalid? The serializer itself handles that logic
* Imagine the data needed when listing games is different from the data needed
when retrieving a game. How would you implement that? A different serializer is called if a single game is retrieve or a Minimum serializer is called whenever you want the entire list of games.
## Delete a game
* How would you handle the case where the ID is invalid? Serializer handles that logic.
* And what about trying to delete a game that’s already deleted? A service is in charge of the deletion and raises an error whenever a Game could not be deleted.


## Cosas que mejoraría:

# Manejo del empate
# Paginación en el listado de Games
# Mayor coverage de tests unitarios
# Manejo de jugadores con nombres repetidos


# TODO:
- Subir a git
- Probar tests unitarios que existen y ver si agregas mas - DONE
- Probar Dockerfile - DONE
- Deploy en EC2?