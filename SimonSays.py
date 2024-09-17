import random
from time import sleep
import ButtonSetup
import pyglet

def simons_sequence_add():
	'''Adds the next button to the game'''
	return(ButtonSetup.SetupPlayerButtons.button_list[random.randint(0, len(ButtonSetup.SetupPlayerButtons.button_list) -1)])

def show_score(score):
	'''calculate score and show in binary'''
	if (score - 16) > 0:
		score = score - 16
		ButtonSetup.SetupPlayerButtons.button_list[0].ledOn()
	if (score - 8) > 0:
		score = score - 8
		ButtonSetup.SetupPlayerButtons.button_list[1].ledOn()
	if (score - 4) > 0:
		score = score - 4
		ButtonSetup.SetupPlayerButtons.button_list[2].ledOn()
	if (score - 2) >= 0:
		score = score - 2
		ButtonSetup.SetupPlayerButtons.button_list[3].ledOn()
	if (score - 1) == 0:
		ButtonSetup.SetupPlayerButtons.button_list[4].ledOn()
	ButtonSetup.SetupPlayerButtons.button_list[0].wait_for_press()

def simon_says_game():
	'''Main loop of the game'''
	sequence = []
	score = 0
	while True:
		sequence.append(simons_sequence_add())
		for button in sequence:
			button.ledBlink(on_time = .75, off_time = .25, count = 1)
		if not player_input(sequence):
			for button in ButtonSetup.SetupPlayerButtons.button_list:
				button.ledBlink(on_time = .2, off_time = .2, count = 10, background = True)
			sleep(5)
			break
		score += 1
	show_score(score)

def player_input(sequence):
	'''What happens on the players turn'''
	player_input_list = []
	index = 0
	while len(player_input_list) < len(sequence):
		for button in ButtonSetup.SetupPlayerButtons.button_list:
			if button.is_pressed:
				button.ledBlink(on_time = .2, off_time = .2, count = 1, background = True)
				player_input_list.append(button)
				if player_input_list[index] != sequence[index]:
					return False
				index += 1
				sleep(.1)
	return True



