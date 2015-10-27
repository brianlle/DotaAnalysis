# zealous-octo-moo
# Python script used to pull up match history of the desired player and then find stats about those matches, such as performance of repeat teammates
# Use dota_request for requesting match data (may take a few hours depending on number of matches); will save data locally so that it does not need to be requested in the future unless more matches have been played
# PlayerID refers to a player's Steam 3 ID for both calling the API (to request a specific player's matches) and for data sorting purposes (player participants listed by ID). Steam 3 IDs can be found using steamidfinder.com by searching the player's name.
