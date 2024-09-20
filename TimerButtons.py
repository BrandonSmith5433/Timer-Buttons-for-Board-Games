from time import sleep, time
import random
import SimonSays , WhackAMole, SoundTest
import ButtonSetup, ExportData

player_button_list = ButtonSetup.SetupPlayerButtons.button_list
auxillary_button_list = ButtonSetup.SetupAcceptButton.auxillary_button_list
active_player_button_list = []
turn_order_button_list = []
time_counter_list = []
turn_in_progress = True
player_selection = False
pause_counter_dict = {}

def gameTracker():
    game_state = "setup"
    while game_state != "complete":
        if game_state == "setup":
            game_state = gameSetup(game_state)
        if game_state == "determine_turn_order":
            game_state = determineTurnOrder(game_state)
        if game_state == "game_round":
            game_state = gameRound(game_state, time_counter_list)
        if game_state == "game_end":
            gameEnd()
            
def gameSetup(game_state):
    '''This function will allow players to determine which buttons will be included in the current game
    the buttons will remain on and can be turned off by pressing, this will remove them from the current 
    game, they can also be turned back on.  Confirmation is on press of the first auxillary button.
    This is also the point at which a custom game can be played by using other auxillary buttons'''

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

    #loop for waiting on confirmation
    while confirm_active_players == False:
        for button in player_button_list:
            button.when_pressed = gameSetupPressed
        for button in auxillary_button_list:
            button.when_pressed = gameSetupAuxillaryPressed
        for button in active_player_button_list:
            button.ledToggle()
        sleep(.2)
        
        
    #Resets button state so that nothing will happen when pressed
    for button in player_button_list:
        button.when_pressed = None
    
    #Returns game_state value to next phase
    return("determine_turn_order")

def determineTurnOrder(game_state):

    global player_selection
    player_selection = False
    
    def determineTurnOrderPressed_Auxillary(button):
        if len(turn_order_button_list) == len(active_player_button_list):
            global player_selection
            player_selection = True

    def determineTurnOrderPressed(button):
        if button in turn_order_button_list:
            turn_order_button_list.remove(button)
            button.ledOff()
        else:
            turn_order_button_list.append(button)
            button.ledOn()

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
        button.ledOff()
    for button in auxillary_button_list:
        button.when_pressed = None
    
    return ("game_round")
    
def gameRound(game_state, time_counter_list):

    ##Creates a list of times for players active in the game
    if not time_counter_list:
        for button in active_player_button_list:
            time_counter_list.append(0)
    
    if not pause_counter_dict:
        x = 0
        for button in active_player_button_list:
            pause_counter_dict.update({button : 0})
            pause_counter_dict.update({("count" + str(x)) : 0})
            x += 1

    round_complete = False
    game_complete = False

    def pause(pause_button):
        '''Allows any player to pause the game and any player to unpause the game.  The time should only count for the active player and will be subtracted from his total turn time
           Secondary function allows us to see who paused the game the longest and the most.'''
        
        resetButtons()

        for button in active_player_button_list:
            if button.activePlayer == True:
                active_player.is_paused = True
                pause_start_time = time()
                button.ledOff()
            
        

        while active_player.is_paused == True:
            
            pause_button.ledOn()

            for button in active_player_button_list:
                button.when_released = unpause
            sleep(.2)
            pause_button.ledOff()
            sleep(.2)
            
        resetButtons()

        active_player.pauseTime += (time() - pause_start_time)
        pause_counter_dict[button] += (time() - pause_start_time)
        pause_counter_dict["count" + str(active_player_button_list.index(button))] += 1

    def unpause(active_player):
        active_player.is_paused = False

    
    def nextTurn(active_player):
        if active_player.held_down == True:
            active_player.held_down = False
        else:
            active_player.activePlayer = False


    def resetButtons():
        for button in active_player_button_list:
            button.when_pressed = None
            button.when_held = None
            button.when_released = None
    
    def endRound():
        nonlocal round_complete
        round_complete == True

    def endGame():
        endRound()
        nonlocal game_complete
        auxillary_button_list[0].when_pressed = None
        auxillary_button_list[0].when_released = None
        auxillary_button_list[0].when_held = None
        game_complete = True
    
    def playerTurn(active_player):

        active_player.pauseTime = 0
        active_player.activePlayer = True
        active_player.ledOn()

        player_turn_start_time = time()

        while active_player.activePlayer == True:
            active_player.when_released = nextTurn
            for button in active_player_button_list:
                button.when_held = pause

        resetButtons()
        active_player.ledOff()
        player_turn_end_time = time()
        total_turn_time = (player_turn_end_time - player_turn_start_time) - active_player.pauseTime
        time_counter_list[active_player_button_list.index(active_player)] += total_turn_time
        ExportData.updateCell(time_counter_list[active_player_button_list.index(active_player)], active_player_button_list.index(active_player))

    active_player = turn_order_button_list[0]
    auxillary_button_list[0].when_released = endRound
    auxillary_button_list[0].when_held = endGame
    playerTurn(active_player)


    while round_complete == False:
        if (turn_order_button_list.index(active_player) + 1) == len(turn_order_button_list):
            active_player = turn_order_button_list[0]
            playerTurn(active_player)
        else:
            active_player = turn_order_button_list[turn_order_button_list.index(active_player) + 1]
            playerTurn(active_player)

    if game_complete == True:
        return("game_end")
    else:
        return("determine_turn_order")

def gameEnd():
    print("game ending")


#SimonSays.simon_says_game()
#WhackAMole.whack_a_mole_game()
#gameTracker()
#soundTest()
    
##below is for testing
#for button in player_button_list:
    #active_player_button_list.append(button)
    #turn_order_button_list.append(button) 
#gameRound('game', time_counter_list)

