import random
from time import sleep, time
import ButtonSetup

def mole1_reset(mole1, break_counter):
	mole1.ledOff()
	score += 1
	break_counter +=1
	return break_counter
	
def mole2_reset(mole2, break_counter):
	mole2.ledOff()
	score += 1
	break_counter +=1
	return break_counter
	
def mole3_reset(mole3, break_counter):
	mole3.ledOff()
	score += 1
	break_counter +=1
	return break_counter
	
def show_score(score):
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

def nextmole():
	'''Adds the next button to the game'''
	return(ButtonSetup.SetupPlayerButtons.button_list[random.randint(0, len(ButtonSetup.SetupPlayerButtons.button_list) -1)])

def whack_a_mole_game():
	moles = 50
	mole_life = 1.5
	respawn = 1
	score = 0
	
	while moles > 0: 
		end_time = time() + mole_life
		mole = nextmole()
		mole.ledOn()
		while time() < end_time:
			if mole.is_pressed:
				mole.ledOff()
				score += 1
				break
		mole_life -= .02
		respawn -=.014
		moles -= 1
		mole.ledOff()
		sleep(respawn)
		print(score)
		
	mole_life = 2
	respawn = .8
	print(score)
	
'''Maybe work on fixing multiple
	while moles > 9:
		print("start of 2")
		end_time = time() + mole_life
		
		mole1 = nextmole()
		mole1.ledOn()
		
		mole2 = nextmole()
		while mole2 == mole1:
			mole2 = nextmole()
		mole2.ledOn()
		
		break_counter = 0
		
		while time() < end_time:
			
			mole1.when_pressed = mole1_reset(mole1, break_counter)
			mole2.when_pressed = mole2_reset(mole2, break_counter)
			
			if break_counter == 2:
				break
				
		if not mole1.ledOn():
			score += 1
		if not mole2.ledOn():
			score += 1
			
		mole_life -= .1
		moles -= 2
		mole1.ledOff()
		mole2.ledOff()
		sleep(respawn)
	
	mole_life = 2	
	while moles > 0:
		print("end of 1")
		end_time = time() + mole_life
		mole1 = nextmole()
		mole1.ledOn()
		mole2 = nextmole()
		while mole2 == mole1:
			mole2 = nextmole()
		mole2.ledOn()
		mole3 = nextmole()
		while mole3 == mole1 or mole3 == mole2:
			mole3 = nextmole()
		mole3.ledOn()
		while time() < end_time:
			mole1.when_pressed = mole1_reset(break_counter)
			mole2.when_pressed = mole2_reset(break_counter)
			mole3.when_pressed = mole3_reset(break_counter)

			if break_counter == 3:
				break
		if not mole1.ledOn():
			score += 1
		if not mole2.ledOn():
			score += 1
		if not mole3.ledOn():
			score += 1
		mole_life -= .1
		moles -= 3
		mole1.ledOff()
		mole2.ledOff()
		mole3.ledOff()
		sleep(respawn)
	show_score(score)
'''
