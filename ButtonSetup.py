from gpiozero import Button, LED
import SoundTest

class SetupPlayerButtons(Button):
	round_count = 0
	active_turn = 0
	enter_pause = False
	button_list = []
	time_list = []
	
	def __init__(self, color, button_pin, led_pin):
		super().__init__(button_pin, bounce_time = .01, hold_time = 1)
		self.led = LED(led_pin)
		self.led.off()
		SetupPlayerButtons.button_list.append(self)
		self.color = color
		self.activePlayer = False 
		self.held_down = False
		self.pauseTime = 0
		self.is_paused = False

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

class SetupBruhButton(Button):
    def __init__(self,button_pin):
        super().__init__(button_pin, bounce_time = .01)
        self.when_pressed = SoundTest.bruh
		
bruh_button = SetupBruhButton(13)
accept_button = SetupAcceptButton(25)
white_button = SetupPlayerButtons("White", 27, 17)
red_button = SetupPlayerButtons("Red", 6, 5)
blue_button = SetupPlayerButtons("Blue", 19, 26)
yellow_button = SetupPlayerButtons("Yellow", 21, 20)
green_button = SetupPlayerButtons("Green", 23, 24)
