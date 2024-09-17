from time import sleep, time
import csv
import random
import SimonSays , WhackAMole, SoundTest
import ButtonSetup#, ExportData

player_button_list = ButtonSetup.SetupPlayerButtons.button_list
auxillary_button_list = ButtonSetup.SetupAcceptButton.auxillary_button_list
active_player_button_list = []
turn_order_button_list = []
time_counter_list = []


def gameTracker():
	game_state = "setup"
	while game_state != "complete":
		if game_state == "setup":
			game_state = gameSetup(game_state)
		if game_state == "determine_turn_order":
			game_state = determineTurnOrder(game_state)
		if game_state == "game_round":
			game_state = gameRound(game_state)
		if game_state == "game_end":
			gameEnd()
		
	
	
def gameSetup(game_state):
	'''This function will allow players to determine which buttons will be included in the current game
	the buttons will remain on and can be turned off by pressing, this will remove them from the current 
	game, they can also be turned back on.  Confirmation is on press of the first auxillary button.
	This is also the point at which a custom game can be played by using other auxillary buttons
	'''
	confirm_active_players = False
	
	#What the buttons will do during setup, pressing a lit button turns it off and removes it from active players
	#and vice versa
	def gameSetupPressed(button):
		if button in active_player_button_list:
			active_player_button_list.remove(button)
			button.ledOff()
		else:
			active_player_button_list.append(button)
			button.ledOn()
		
	#What auxillary buttons will do, the first (main) will start the game, others will do other programs	
	def gameSetupAuxillaryPressed(button):
		if button == auxillary_button_list[0]:
			nonlocal confirm_active_players
			confirm_active_players = True
		#if button == auxillary_button_list[1]:
		#	SimonSays.simon_says_game()
		#if button == auxillary_button_list[2]:
		#	WhackAMole.whack_a_mole_game()
			
	#Setup lights (Not needed, but is fun)
	for button in player_button_list:
		button.ledBlink(on_time = .01, off_time = .01, count = 5, background = False)
	for button in player_button_list:
		button.ledBlink(on_time = .02, off_time = .02, count = 5, background = True)
	sleep(1.5)
	
	#Turns all buttons on and adds them to active players
	for button in player_button_list:
		button.ledOn()
		active_player_button_list.append(button)
	
	#loop for waiting on confirmation
	while confirm_active_players == False:
		for button in player_button_list:
			button.when_pressed = gameSetupPressed
		for button in auxillary_button_list:
			button.when_pressed = gameSetupAuxillaryPressed
		sleep(.2)
	
	#Resets button state so that nothing will happen when pressed
	for button in player_button_list:
		button.when_pressed = None
		
	#Returns game_state value to next phase
	return("determine_turn_order")
	
def determineTurnOrder(game_state):
	
	player_selection = False
	
	def determineTurnOrderPressed_Auxillary(button):
		nonlocal player_selection
		if len(turn_order_button_list) == len(active_player_button_list):
			player_selection = True
		
	def determineTurnOrderPressed(button):
		if button in turn_order_button_list:
			turn_order_button_list.remove(button)
			print("remove")
		else:
			turn_order_button_list.append(button)
			print("add")
		for button in turn_order_button_list:
			button.ledBlink(on_time = .05, off_time = .3, count = (turn_order_button_list.index(button) + 1), background = True)
		sleep(len(turn_order_button_list)*.35)
			
	for button in active_player_button_list:
		button.ledBlink(on_time = .2, off_time = .2, count = 10, background = True)
	sleep(2)
	for button in active_player_button_list:
		button.ledOff()
		
	while player_selection == False:
		for button in active_player_button_list:
			button.when_pressed = determineTurnOrderPressed
		for button in auxillary_button_list:
			button.when_pressed = determineTurnOrderPressed_Auxillary
	
	#Resets button state so that nothing will happen when pressed
	for button in player_button_list:
		button.when_pressed = None
	for button in auxillary_button_list:
		button.when_pressed = None	
	
	return ("game_round")
	
def gameRound(game_state):
	if not time_counter_list:
		time_counter_list = active_player_button_list.copy()
	turn_in_progress = False
	round_complete = False
	game_complete = False

	auxillary_button_list[0].when_released = endRound
	auxillary_button_list[0].when_held = endGame

	#Causes LEDS to blink for player postion... First blinks one time, Second blinks 2 times, etc.
	for button in turn_order_button_list:
		button.ledBlink(on_time = .15, off_time = .2, count = (turn_order_button_list.index(button) + 1), background = True)
	
	#First player at start of the round
	active_player = turn_order_button_list[0]
	playerTurn(active_player)

	def playerTurn(active_player):
		player_turn_start_time = time()
		total_pause_time = 0
		while turn_in_progress == True:
			active_player.when_released = nextTurn(active_player, turn_in_progress)
			for button in active_player_button_list:
				button.when_held = pause(active_player, total_pause_time)
		player_turn_end_time = time()
		total_turn_time = (player_turn_end_time - player_turn_start_time) - total_pause_time
		time_counter_list[active_player_button_list.indexOf(active_player)] += total_turn_time
		ExportData.UpdateCell(time_counter_list[active_player_button_list.indexOf(active_player)], active_player_button_list.indexOf(active_player))
		
	def pause(active_player, total_pause_time):
		pause_active = True
		pause_start_time = time()
		resetButtons()
		while pause_active == True:
			for button in active_player_button_list:
				button.when_pressed = unpause(pause_active)
		resetButtons()
		return ((time() - pause_start_time)+ total_pause_time)

	def unpause(button, pause_active):
		pause_active = False
		return(pause)
	
	def nextTurn(active_player, turn_in_progress):
		resetButtons()
		turn_in_progress = False
		return(turn_in_progress)

	def resetButtons():
		for button in active_player_button_list:
			button.when_pressed = None
			button.when_held = None
			button.when_released = None
	
	def endRound():
		round_complete == True
		
	def endGame():
		nonlocal game_complete
		auxillary_button_list[0].when_pressed = None
		auxillary_button_list[0].when_released = None
		auxillary_button_list[0].when_held = None
		game_complete = True

	while round_complete == False:
		if (active_player_button_list.indexOf(active_player) + 1) == len(active_player_button_list):
			active_player = active_player_button_list[0]
			playerTurn(active_player)
		else:
			active_player = active_player_button_list[active_player_button_list.indexOf(active_player) + 1]
			playerTurn(active_player)

	if game_complete == True:
		return("game_end")
	else:
		return("determine_turn_order")

def gameEnd():
	print("game ending")
	with open('testcsv.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['player Color', 'Total Time'])
		for i in range(len(active_player_button_list)):
			writer.writerow([active_player_button_list[i].color, time_counter_list[i]])


#SimonSays.simon_says_game()
#WhackAMole.whack_a_mole_game()
gameTracker()
#soundTest()

