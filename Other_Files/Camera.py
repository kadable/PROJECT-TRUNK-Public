from General_Functions import *

class Camera():
    """
    Lags behind player, x and y used to calculate x and ys for blitting
    """
    def __init__(self): #Should only have self and level_size
        self.reset(0,0)
    def follow(self,player,level_width,level_height):
        #Player at the centre of the screen
        self.x_destination = player.x - self.screen_width/2
        self.y_destination = player.y - self.screen_height/2
        #How much camera moves this frame, lags behind player
        self.hsp = round((self.x_destination - self.x)*0.2)
        self.vsp = round((self.y_destination - self.y)*0.2)
        #Move Camera
        self.x += self.hsp
        self.y += self.vsp
        #Clamp to level size
        self.x = clamp(self.x,0,level_width - self.screen_width)
        self.y = clamp(self.y,0,level_height - self.screen_height)
    def reset(self,start_x,start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.x = self.start_x
        self.y = self.start_y
        self.x_destination = 0
        self.y_destination = 0
        self.hsp = 0
        self.vsp = 0
        self.screen_width,self.screen_height = pygame.display.get_surface().get_size()
        
   
