from General_Functions import *

class Pause_Menu():
    def __init__(self):
        #State
        self.just_paused = True
        #Images
        self.background_image = None
        self.play_image_normal = pygame.image.load("Images/UI/pause_play.png").convert_alpha()
        self.play_image_on_hover = pygame.image.load("Images/UI/pause_play_on_hover.png").convert_alpha()
        self.play_image = self.play_image_normal
        self.play_rect = pygame.image.load("Images/UI/pause_play.png").get_rect()
        self.play_rect.x = 180
        self.play_rect.y = 210
        self.quit_image_normal = pygame.image.load("Images/UI/pause_quit.png").convert_alpha()
        self.quit_image_on_hover = pygame.image.load("Images/UI/pause_quit_on_hover.png").convert_alpha()
        self.quit_image = self.quit_image_normal
        self.quit_rect = pygame.image.load("Images/UI/pause_quit.png").get_rect()
        self.quit_rect.x = 520
        self.quit_rect.y = 220
        self.save_image_normal = pygame.image.load("Images/UI/pause_save.png").convert_alpha()
        self.save_image_on_hover = pygame.image.load("Images/UI/pause_save_on_hover.png").convert_alpha()
        self.save_image = self.save_image_normal
        self.save_rect = pygame.image.load("Images/UI/pause_save.png").get_rect()
        self.save_rect.x = 0
        self.save_rect.y = 510
        self.reset_save_image_normal = pygame.image.load("Images/UI/pause_reset_save.png").convert_alpha()
        self.reset_save_image_on_hover = pygame.image.load("Images/UI/pause_reset_save_on_hover.png").convert_alpha()
        self.reset_save_image = self.reset_save_image_normal 
        self.reset_save_rect = pygame.image.load("Images/UI/pause_reset_save.png").get_rect()
        self.reset_save_rect.x = 780
        self.reset_save_rect.y = 510
        #Inputs
        self.mouse_pos = None
        self.left_click_down = None
        self.pause_key = None
        #Pointer
        self.pointer_animation = [[pygame.image.load("Images/Player/pointer_1.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_2.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_3.png").convert_alpha(),5],
                                  ] 
        self.pointer_rect = self.pointer_animation[0][0].get_rect() #Just for centering it
        self.pointer_current_frame = [0,0]
    def update(self,game_state_manager,input_dict,tilemap_level_name):
        #Unlock mouse from screen
        pygame.event.set_grab(False)
        #Update buttons
        self.mouse_pos = input_dict["mouse_pos"]
        self.left_click_down = input_dict["left_click_down"]
        self.pause_key = input_dict["pause_key"]
        if self.pause_key:
            game_state_manager.state = game_state_manager.states["Normal"]
            pygame.event.set_grab(True)
            self.just_paused = True
        if self.play_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                game_state_manager.state = game_state_manager.states["Normal"]
                pygame.event.set_grab(True)
                self.just_paused = True
            self.play_image = self.play_image_on_hover
        else:
            self.play_image = self.play_image_normal
        if self.quit_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                game_state_manager.state = game_state_manager.states["Menu"]
                pygame.event.set_grab(True)
                self.just_paused = True
            self.quit_image = self.quit_image_on_hover
        else:
            self.quit_image = self.quit_image_normal
        if self.save_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                save_file = open("Save/save.json","w")
                json.dump({"start_level":tilemap_level_name},save_file)
                save_file.close()
            self.save_image = self.save_image_on_hover
        else:
            self.save_image = self.save_image_normal
        if self.reset_save_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                save_file = open("Save/save.json","w")
                #json.dump({"start_level":"Levels/world_1/level_1/level_1","intro_played":False},save_file)
                json.dump({"start_level":"Levels/world_1/level_1/level_1","intro_played":True},save_file)
                save_file.close()
            self.reset_save_image = self.reset_save_image_on_hover
        else:
            self.reset_save_image = self.reset_save_image_normal
    def draw(self,screen):
        if self.just_paused:
            self.background_image = screen.convert()
            self.background_image.fill((50,50,50,10), special_flags=pygame.BLEND_ADD)
            self.just_paused = False
        screen.blit(self.background_image,(0,0))
        screen.blit(self.play_image,(self.play_rect.x,self.play_rect.y))
        screen.blit(self.quit_image,(self.quit_rect.x,self.quit_rect.y))
        screen.blit(self.save_image,(self.save_rect.x,self.save_rect.y))
        screen.blit(self.reset_save_image,(self.reset_save_rect.x,self.reset_save_rect.y))
        #Mouse
        if self.mouse_pos:
            self.pointer_rect.centerx = self.mouse_pos[0]
            self.pointer_rect.centery = self.mouse_pos[1]
            self.pointer_current_frame = animation(self.pointer_animation,self.pointer_current_frame)
            screen.blit(self.pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))
        

