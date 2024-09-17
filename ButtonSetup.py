from gpiozero import Button, LED

class SetupPlayerButtons(Button):
	round_count = 0
	active_turn = 0
	enter_pause = False
	button_list = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .01)
		self.led = LED(led_pin)
		self.led.off()
		SetupPlayerButtons.button_list.append(self)
		self.color = color

	def buttonHold(self):
		'''What is done when a colored button is held'''
		game_state = SetupPlayerButtons.game_state
		match game_state:
			case 4: #Active gameplay
				if self.is_live:
					self.held = True
					SetupPlayerButtons.enter_pause = True

	def buttonRelease(self):
		'''What is done when a colored button is released'''
		game_state = SetupPlayerButtons.game_state
		match game_state:
			case 4: #Active gameplay
				if self.is_live:
					if self.held == True & self.count == 1:
						self.held = False
						self.count = 0
						SetupPlayerButtons.enter_pause = False
					elif self.held == True:
						self.count = 1
					else:
						SetupPlayerButtons.active_turn = 1

	def ledOn(self):
		self.led.on()
			
	def ledOff(self):
		self.led.off()
		
	def ledToggle(self):
		self.led.toggle()
			
	def ledBlink(self, on_time = 1, off_time = 1, count = 3, background = False):
		self.led.blink(on_time = on_time,off_time = off_time ,n = count, background = background)
	
class SetupAcceptButton(Button):
	
	auxillary_button_list = []
	
	def __init__(self,button_pin):
		
		super().__init__(button_pin, bounce_time = .01)
		SetupAcceptButton.auxillary_button_list.append(self)
		self.held = False
		

accept_button = SetupAcceptButton(25)
white_button = SetupPlayerButtons("White", 27, 17)
red_button = SetupPlayerButtons("Red", 6, 5)
blue_button = SetupPlayerButtons("Blue", 19, 26)
yellow_button = SetupPlayerButtons("Yellow", 21, 20)
green_button = SetupPlayerButtons("Green", 23, 24)
