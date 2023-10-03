# ErinyCatcher
ErinyCatcher
This is a script that sends notifications when your friend is in the game (League of Legends).

## Purpose

It was created to catch our friend who entered the game and did not invite us to the game.

### How does it work?
Searches for the previously named summoner via the Riot Developer API. First, the user's ID is found. Then, checking whether the user is in the game or not is done with the API. If the user is in the game, a notification is created using win10toast.

