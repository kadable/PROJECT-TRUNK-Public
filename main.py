import sys
sys.path.insert(0,"Other_Files")
from General_Functions import *
from Game_State_Manager import *
from Inputs import *
from Player import *
from Camera import *
from Tilemap import *
from Instances import *
from Main_Menu import *
from Pause_Menu import *
from Death_Screen import *

"""
Inits and runs the game.
"""

pygame.init()

pygame.display.set_caption("PROJECT TRUNK")
clock = pygame.time.Clock()
 
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((1024,576),pygame.SCALED,vsync=1)
 
#Lock mouse in screen
pygame.event.set_grab(True)

#Init
game_state_manager = Game_State_Manager()
player = Player(0,0)
player_bullets = Bullets(player=True)
camera = Camera() 
tilemap = Tilemap()
instances = Instances()
enemy_bullets = Bullets()
input_dict = None
controller = False
menu = Menu()
intro_cutscene = Intro_Cutscene()
ending_cutscene = Ending_Cutscene() 
pause_menu = Pause_Menu()
death_screen = Death_Screen()

#Main Game Loop
while True:
    #Get Inputs
    input_dict,controller = inputs(controller)
    #Update
    game_state_manager.update(input_dict,player,player_bullets,camera,tilemap,instances,enemy_bullets,menu,intro_cutscene,ending_cutscene,pause_menu,death_screen)
    #Draw
    game_state_manager.draw(screen,player,player_bullets,camera,tilemap,instances,enemy_bullets,menu,intro_cutscene,ending_cutscene,pause_menu,death_screen)
    #Update Screen 
    pygame.display.flip()
    #FPS
    clock.tick_busy_loop(60)
    #print(clock.get_fps())
