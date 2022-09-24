from General_Functions import *

class Death_Screen():
    def __init__(self):
        #State
        self.just_died = True
        #Images
        self.background_image = None
        self.death_screen_animation = [[pygame.image.load("Images/UI/death_screen_1.png").convert_alpha(),5],[pygame.image.load("Images/UI/death_screen_2.png").convert_alpha(),5],[pygame.image.load("Images/UI/death_screen_3.png").convert_alpha(),5]]
        self.death_screen_current_frame = [0,0]
        self.death_messages = [pygame.image.load("Images/UI/death_message_1.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_2.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_3.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_4.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_5.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_6.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_7.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_8.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_9.png").convert_alpha(),
                               pygame.image.load("Images/UI/death_message_10.png").convert_alpha(),
                              ]
        self.current_death_message_index = None
        #Inputs
        self.mouse_pos = None
        self.left_click_down = None
        self.controller = False
        self.shooting_key = None
        self.controller_trigger_held = False
        #Pointer
        self.pointer_animation = [[pygame.image.load("Images/Player/pointer_1.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_2.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_3.png").convert_alpha(),5],
                                  ] 
        self.pointer_rect = self.pointer_animation[0][0].get_rect() #Just for centering it
        self.pointer_current_frame = [0,0]
    def update(self,game_state_manager,input_dict):
        #Unlock mouse from screen
        pygame.event.set_grab(False)
        #Update buttons
        self.mouse_pos = input_dict["mouse_pos"]
        self.left_click_down = input_dict["left_click_down"]
        self.controller = input_dict["controller"]
        if self.controller:
            #Have to do this shenagians because no keydown for controller triggers
            self.shooting_key = False
            if not input_dict["shooting_key"] and self.controller_trigger_held:
                print("TRUE")
                self.controller_trigger_held = False
            if input_dict["shooting_key"] and not self.controller_trigger_held:
                self.shooting_key = True
        if self.left_click_down or (self.controller and self.shooting_key):
            game_state_manager.state = game_state_manager.states["Reset Level"]
            pygame.event.set_grab(True)
            self.just_died = True
    def draw(self,screen):
        if self.just_died:
            self.background_image = screen.convert()
            self.background_image.fill((50,50,50,10), special_flags=pygame.BLEND_ADD)
            self.current_death_message_index = random.randint(0,len(self.death_messages)-1)
            self.just_died = False
        self.death_screen_current_frame = animation(self.death_screen_animation,self.death_screen_current_frame)
        screen.blit(self.background_image,(0,0))
        screen.blit(self.death_screen_animation[self.death_screen_current_frame[0]][0],(0,0))
        screen.blit(self.death_messages[self.current_death_message_index],(260,440))
        #Mouse
        if self.mouse_pos:
            self.pointer_rect.centerx = self.mouse_pos[0]
            self.pointer_rect.centery = self.mouse_pos[1]
            self.pointer_current_frame = animation(self.pointer_animation,self.pointer_current_frame)
            screen.blit(self.pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))
        

