from General_Functions import *


class Menu():
    def __init__(self):
        #Images
        self.main_menu_image = pygame.image.load("Images/UI/main_menu_1.png").convert_alpha()
        self.main_menu_animation = [
                                        [pygame.image.load("Images/UI/main_menu_1.png").convert_alpha(),5],
                                        [pygame.image.load("Images/UI/main_menu_2.png").convert_alpha(),5],
                                        [pygame.image.load("Images/UI/main_menu_3.png").convert_alpha(),5],
                                    ]
        #Speech Bubble (Play)
        self.speech_bubble_animation_normal = [
                                [pygame.image.load("Images/UI/speech_bubble_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/speech_bubble_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/speech_bubble_3.png").convert_alpha(),5],

                             ]
        self.speech_bubble_animation_on_hover = [
                                [pygame.image.load("Images/UI/speech_bubble_on_hover_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/speech_bubble_on_hover_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/speech_bubble_on_hover_3.png").convert_alpha(),5],
                             ]
        self.speech_bubble_animation = self.speech_bubble_animation_normal
        self.speech_bubble_current_frame = [0,0]
        self.speech_bubble_rect = pygame.image.load("Images/UI/speech_bubble_1.png").get_rect() 
        self.speech_bubble_rect.x = 365
        self.speech_bubble_rect.y = 380
        #Door (Exit)
        self.door_animation_normal = [
                                [pygame.image.load("Images/UI/door_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/door_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/door_3.png").convert_alpha(),5],
                             ]
        self.door_animation_on_hover = [
                                [pygame.image.load("Images/UI/door_on_hover_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/door_on_hover_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/door_on_hover_3.png").convert_alpha(),5],
                             ]
        self.door_animation = self.door_animation_normal
        self.door_current_frame = [0,0]
        self.door_rect = pygame.image.load("Images/UI/door_1.png").get_rect() 
        self.door_rect.x = 0
        self.door_rect.y = 484
        #TV (Intro Cutscene)                        
        self.tv_animation_normal = [
                                [pygame.image.load("Images/UI/television_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/television_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/television_3.png").convert_alpha(),5],
                             ]
        self.tv_animation_on_hover = [
                                [pygame.image.load("Images/UI/television_on_hover_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/television_on_hover_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/UI/television_on_hover_3.png").convert_alpha(),5],
                             ]
        self.tv_animation = self.tv_animation_normal
        self.tv_current_frame = [0,0]
        self.tv_rect = pygame.image.load("Images/UI/television_1.png").get_rect()
        self.tv_rect.x = 890
        self.tv_rect.y = 470
        #Background
        self.background = {
            "main_menu_background_1":{
                "image":pygame.image.load("Images/UI/main_menu_background_1.png").convert(),
                "start_x":0,
                "start_y":0,
                "x_offset":0,
                "y_offset":0,
                "lag":0,
                "length":1024},
            "main_menu_background_2":{
                "image":pygame.image.load("Images/UI/main_menu_background_2.png").convert_alpha(),
                "start_x":0,
                "start_y":0,
                "y_offset":100,
                "lag":0.25,
                "length":1024,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
            "main_menu_background_3":{
                "image":pygame.image.load("Images/UI/main_menu_background_3.png").convert_alpha(),
                "start_x":0,
                "start_y":0,
                "y_offset":100,
                "lag":0.5,
                "length":1024,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
        }
        self.background_layer_1 = self.background["main_menu_background_1"]
        self.background_layer_2 = self.background["main_menu_background_2"]
        self.background_layer_3 = self.background["main_menu_background_3"]
        self.x_position = 0
        self.ship_x_for_sin = 0 #So ship bobs up and down
        self.ship_y = 50
        self.current_frame = [0,0]
        #Inputs
        self.mouse_pos = None
        self.left_click_down = None
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
        self.x_position += 30
        if self.x_position >= 2147483646:
            self.x_position = 0
        self.ship_x_for_sin += 1
        if self.ship_x_for_sin >= 2147483646:
            self.ship_x_for_sin = 0
        self.ship_y = 50 + (math.sin(self.ship_x_for_sin * 1/15) * 10)
        self.speech_bubble_rect.y = 380 + (math.sin(self.ship_x_for_sin * 1/15) * 10)
        #Update background
        self.background_layer_1["x_offset"] = 0
        self.background_layer_1["y_offset"] = 0
        #Layer 2
        self.background_layer_2["x_offset_1"] = round((-self.x_position)*self.background_layer_2["lag"]) + (self.background_layer_2["x_offset_multiplier"] * self.background_layer_2["length"]) + self.background_layer_2["start_x"]
        self.background_layer_2["x_offset_2"] = (round((-self.x_position)*self.background_layer_2["lag"]) + self.background_layer_2["length"]) + (self.background_layer_2["x_offset_multiplier"] * self.background_layer_2["length"]) + self.background_layer_2["start_x"]
        if self.background_layer_2["x_offset_1"] <= -self.background_layer_2["length"]:
            self.background_layer_2["x_offset_multiplier"] += 1
        elif self.background_layer_2["x_offset_2"] >= self.background_layer_2["length"]:
            self.background_layer_2["x_offset_multiplier"] -= 1
        #Layer 3
        self.background_layer_3["x_offset_1"] = round((-self.x_position)*self.background_layer_3["lag"]) + (self.background_layer_3["x_offset_multiplier"] * self.background_layer_3["length"]) + self.background_layer_3["start_x"]
        self.background_layer_3["x_offset_2"] = (round((-self.x_position)*self.background_layer_3["lag"]) + self.background_layer_3["length"]) + (self.background_layer_3["x_offset_multiplier"] * self.background_layer_3["length"]) + self.background_layer_3["start_x"]
        if self.background_layer_3["x_offset_1"] <= -self.background_layer_3["length"]:
            self.background_layer_3["x_offset_multiplier"] += 1
        elif self.background_layer_3["x_offset_2"] >= self.background_layer_3["length"]:
            self.background_layer_3["x_offset_multiplier"] -= 1
        #Update buttons
        self.mouse_pos = input_dict["mouse_pos"]
        self.left_click_down = input_dict["left_click_down"]
        if self.speech_bubble_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                game_state_manager.state = game_state_manager.states["Start Game"]
                #Lock mouse to screen
                pygame.event.set_grab(True)
            if self.speech_bubble_animation != self.speech_bubble_animation_on_hover:
                self.speech_bubble_animation = self.speech_bubble_animation_on_hover
        elif self.speech_bubble_animation != self.speech_bubble_animation_normal:
            self.speech_bubble_animation = self.speech_bubble_animation_normal
        if self.door_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:  
                pygame.quit()
                sys.exit()
            if self.door_animation != self.door_animation_on_hover:
                self.door_animation = self.door_animation_on_hover
        elif self.door_animation != self.door_animation_normal:
            self.door_animation = self.door_animation_normal
        if self.tv_rect.collidepoint(self.mouse_pos):
            if self.left_click_down:
                save_file_dict = json.load(open("Save/save.json","r"))
                save_file_dict["intro_played"] = True
                save_file = open("Save/save.json","w")
                json.dump(save_file_dict,save_file)
                save_file.close()
                game_state_manager.state = game_state_manager.states["Intro Cutscene"]
            if self.tv_animation != self.tv_animation_on_hover:
                self.tv_animation = self.tv_animation_on_hover
                self.tv_current_frame = [0,0]
        elif self.tv_animation != self.tv_animation_normal:
            self.tv_animation = self.tv_animation_normal
            self.tv_current_frame = [0,0]
    def draw(self,screen):
        #Background
        screen.blit(self.background_layer_1["image"],(self.background_layer_1["x_offset"],self.background_layer_1["y_offset"]))
        screen.blit(self.background_layer_2["image"],(self.background_layer_2["x_offset_1"],self.background_layer_2["y_offset"]))
        screen.blit(self.background_layer_2["image"],(self.background_layer_2["x_offset_2"],self.background_layer_2["y_offset"]))
        screen.blit(self.background_layer_3["image"],(self.background_layer_3["x_offset_1"],self.background_layer_3["y_offset"]))
        screen.blit(self.background_layer_3["image"],(self.background_layer_3["x_offset_2"],self.background_layer_3["y_offset"]))
        self.current_frame = animation(self.main_menu_animation,self.current_frame)
        #Main Menu
        self.main_menu_image = self.main_menu_animation[self.current_frame[0]][0]
        screen.blit(self.main_menu_image,(200,self.ship_y))
        #Speech Bubble
        self.speech_bubble_current_frame = animation(self.speech_bubble_animation,self.speech_bubble_current_frame)
        screen.blit(self.speech_bubble_animation[self.speech_bubble_current_frame[0]][0],(self.speech_bubble_rect.x,self.speech_bubble_rect.y))
        #Door
        self.door_current_frame = animation(self.door_animation,self.door_current_frame)
        screen.blit(self.door_animation[self.door_current_frame[0]][0],(self.door_rect.x,self.door_rect.y))
        #TV
        self.tv_current_frame = animation(self.tv_animation,self.tv_current_frame)
        screen.blit(self.tv_animation[self.tv_current_frame[0]][0],(self.tv_rect.x,self.tv_rect.y))
        #Mouse
        self.pointer_rect.centerx = self.mouse_pos[0]
        self.pointer_rect.centery = self.mouse_pos[1]
        self.pointer_current_frame = animation(self.pointer_animation,self.pointer_current_frame)
        screen.blit(self.pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))

class Intro_Cutscene():
    def __init__(self):
        self.intro_1 = [
                        [pygame.image.load("Images/Cutscenes/intro_1_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_1_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_1_3.png").convert(),5],
                        ]
        self.intro_2 = [
                        [pygame.image.load("Images/Cutscenes/intro_2_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_2_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_2_3.png").convert(),5],
                        ]
        self.intro_3 = [
                        [pygame.image.load("Images/Cutscenes/intro_3_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_3_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_3_3.png").convert(),5],
                        ]
        self.intro_4 = [
                        [pygame.image.load("Images/Cutscenes/intro_4_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_4_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_4_3.png").convert(),5],
                        ]
        self.intro_5 = [
                        [pygame.image.load("Images/Cutscenes/intro_5_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_5_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_5_3.png").convert(),5],
                        ]
        self.intro_6 = [
                        [pygame.image.load("Images/Cutscenes/intro_6_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_6_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_6_3.png").convert(),5],
                        ]
        self.intro_7 = [
                        [pygame.image.load("Images/Cutscenes/intro_7_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_7_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_7_3.png").convert(),5],
                        ]
        self.intro_8 = [
                        [pygame.image.load("Images/Cutscenes/intro_8_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_8_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_8_3.png").convert(),5],
                        ]
        self.intro_9 = [
                        [pygame.image.load("Images/Cutscenes/intro_9_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_9_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_9_3.png").convert(),5],
                        ]
        self.intro_10 = [
                        [pygame.image.load("Images/Cutscenes/intro_10_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_10_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_10_3.png").convert(),5],
                        ]
        self.intro_11 = [
                        [pygame.image.load("Images/Cutscenes/intro_11_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_11_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_11_3.png").convert(),5],
                        ]
        self.intro_12 = [
                        [pygame.image.load("Images/Cutscenes/intro_12_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_12_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_12_3.png").convert(),5],
                        ]
        self.intro_13 = [
                        [pygame.image.load("Images/Cutscenes/intro_13_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_13_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_13_3.png").convert(),5],
                        ]
        self.intro_14 = [
                        [pygame.image.load("Images/Cutscenes/intro_14_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_14_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_14_3.png").convert(),5],
                        ]
        self.intro_15 = [
                        [pygame.image.load("Images/Cutscenes/intro_15_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_15_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_15_3.png").convert(),5],
                        ]
        self.intro_16 = [
                        [pygame.image.load("Images/Cutscenes/intro_16_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_16_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_16_3.png").convert(),5],
                        ]
        self.intro_17 = [
                        [pygame.image.load("Images/Cutscenes/intro_17_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_17_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_17_3.png").convert(),5],
                        ]
        self.intro_18 = [
                        [pygame.image.load("Images/Cutscenes/intro_18_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_18_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/intro_18_3.png").convert(),5],
                        ]
        self.screens = [self.intro_1,self.intro_2,self.intro_3,self.intro_4,self.intro_5,self.intro_6,self.intro_7,self.intro_8,self.intro_9,self.intro_10,self.intro_11,self.intro_12,self.intro_13,self.intro_14,self.intro_15,self.intro_16,self.intro_17,self.intro_18]
        self.current_frame = [0,0]
        self.current_screen = 0
        #Inputs
        self.mouse_pos = None
        self.left_click_down = None
        #Pointer
        self.pointer_animation = [[pygame.image.load("Images/Player/big_pointer_1.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/big_pointer_2.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/big_pointer_3.png").convert_alpha(),5],
                                  ] 
        self.pointer_rect = self.pointer_animation[0][0].get_rect() #Just for centering it
        self.pointer_current_frame = [0,0]
    def update(self,game_state_manager,input_dict):
        #Unlock mouse from screen
        pygame.event.set_grab(False)
        self.mouse_pos = input_dict["mouse_pos"]
        self.left_click_down = input_dict["left_click_down"]
        self.current_frame = animation(self.screens[self.current_screen],self.current_frame)
        if self.left_click_down:
            self.current_screen += 1
            self.current_frame = [0,0]
            if self.current_screen > len(self.screens) - 1:
                self.current_screen = 0
                save_file_dict = json.load(open("Save/save.json","r"))
                #If when play button pressed without intro being played
                if save_file_dict["intro_played"] == False:
                    save_file_dict["intro_played"] = True
                    save_file = open("Save/save.json","w")
                    json.dump(save_file_dict,save_file)
                    save_file.close()
                    game_state_manager.state = game_state_manager.states["Start Game"]
                else:
                    game_state_manager.state = game_state_manager.states["Menu"]
    def draw(self,screen):
        screen.blit(self.screens[self.current_screen][self.current_frame[0]][0],(0,0))
        #Mouse
        if self.mouse_pos:
            self.pointer_rect.centerx = self.mouse_pos[0]
            self.pointer_rect.centery = self.mouse_pos[1]
            self.pointer_current_frame = animation(self.pointer_animation,self.pointer_current_frame)
            screen.blit(self.pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))

class Ending_Cutscene():
    def __init__(self):
        self.ending_1 = [
                        [pygame.image.load("Images/Cutscenes/ending_1_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_1_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_1_3.png").convert(),5],
                        ]
        self.ending_2 = [
                        [pygame.image.load("Images/Cutscenes/ending_2_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_2_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_2_3.png").convert(),5],
                        ]
        self.ending_3 = [
                        [pygame.image.load("Images/Cutscenes/ending_3_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_3_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_3_3.png").convert(),5],
                        ]
        self.ending_4 = [
                        [pygame.image.load("Images/Cutscenes/ending_4_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_4_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_4_3.png").convert(),5],
                        ]
        self.ending_5 = [
                        [pygame.image.load("Images/Cutscenes/ending_5_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_5_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_5_3.png").convert(),5],
                        ]
        self.ending_6 = [
                        [pygame.image.load("Images/Cutscenes/ending_6_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_6_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_6_3.png").convert(),5],
                        ]
        self.ending_7 = [
                        [pygame.image.load("Images/Cutscenes/ending_7_1.png").convert(),6],
                        [pygame.image.load("Images/Cutscenes/ending_7_2.png").convert(),6],
                        [pygame.image.load("Images/Cutscenes/ending_7_3.png").convert(),6],
                        ]
        self.ending_8 = [
                        [pygame.image.load("Images/Cutscenes/ending_8_1.png").convert(),7],
                        [pygame.image.load("Images/Cutscenes/ending_8_2.png").convert(),7],
                        [pygame.image.load("Images/Cutscenes/ending_8_3.png").convert(),7],
                        ]
        self.ending_9 = [
                        [pygame.image.load("Images/Cutscenes/ending_9_1.png").convert(),8],
                        [pygame.image.load("Images/Cutscenes/ending_9_2.png").convert(),8],
                        [pygame.image.load("Images/Cutscenes/ending_9_3.png").convert(),8],
                        ]
        self.ending_10 = [
                        [pygame.image.load("Images/Cutscenes/ending_10_1.png").convert(),9],
                        [pygame.image.load("Images/Cutscenes/ending_10_2.png").convert(),9],
                        [pygame.image.load("Images/Cutscenes/ending_10_3.png").convert(),9],
                        ]
        self.ending_11 = [
                        [pygame.image.load("Images/Cutscenes/ending_11_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_11_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_11_3.png").convert(),10],
                        ]
        self.ending_12 = [
                        [pygame.image.load("Images/Cutscenes/ending_12_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_12_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_12_3.png").convert(),10],
                        ]
        self.ending_13 = [
                        [pygame.image.load("Images/Cutscenes/ending_13_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_13_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_13_3.png").convert(),10],
                        ]
        self.ending_14 = [
                        [pygame.image.load("Images/Cutscenes/ending_14_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_3.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_4.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_5.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_6.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_7.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_8.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_9.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_10.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_11.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_14_12.png").convert(),10],
                        ]
        self.ending_15 = [
                        [pygame.image.load("Images/Cutscenes/ending_15_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_3.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_4.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_5.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_6.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_7.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_8.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_9.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_10.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_11.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_15_12.png").convert(),10],
                        ]
        self.ending_16 = [
                        [pygame.image.load("Images/Cutscenes/ending_16_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_16_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_16_3.png").convert(),10],
                        ]
        self.ending_17 = [
                        [pygame.image.load("Images/Cutscenes/ending_17_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_17_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_17_3.png").convert(),10],
                        ]
        self.ending_18 = [
                        [pygame.image.load("Images/Cutscenes/ending_18_1.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_18_2.png").convert(),10],
                        [pygame.image.load("Images/Cutscenes/ending_18_3.png").convert(),10],
                        ]
        self.ending_19 = [
                        [pygame.image.load("Images/Cutscenes/ending_19_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_19_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_19_3.png").convert(),5]
                        ]
        self.ending_20 = [
                        [pygame.image.load("Images/Cutscenes/ending_20_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_20_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_20_3.png").convert(),5]
                        ]
        self.ending_21 = [
                        [pygame.image.load("Images/Cutscenes/ending_21_1.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_21_2.png").convert(),5],
                        [pygame.image.load("Images/Cutscenes/ending_21_3.png").convert(),5]
                        ]
        self.screens = [self.ending_1,self.ending_2,self.ending_3,self.ending_4,self.ending_5,self.ending_6,self.ending_7,self.ending_8,self.ending_9,self.ending_10,self.ending_11,self.ending_12,self.ending_13,self.ending_14,self.ending_15,self.ending_16,self.ending_17,self.ending_18,self.ending_19,self.ending_20,self.ending_21]
        self.current_frame = [0,0]
        self.current_screen = 0
        #Inputs
        self.mouse_pos = None
        self.left_click_down = None
        #Pointer
        self.pointer_animation = [[pygame.image.load("Images/Player/big_pointer_1.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/big_pointer_2.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/big_pointer_3.png").convert_alpha(),5],
                                  ] 
        self.pointer_rect = self.pointer_animation[0][0].get_rect() #Just for centering it
        self.pointer_current_frame = [0,0]
    def update(self,game_state_manager,input_dict):
        #Unlock mouse from screen
        pygame.event.set_grab(False)
        self.mouse_pos = input_dict["mouse_pos"]
        self.left_click_down = input_dict["left_click_down"]
        self.current_frame = animation(self.screens[self.current_screen],self.current_frame)
        if self.left_click_down:
            self.current_screen += 1
            self.current_frame = [0,0]
            if self.current_screen > len(self.screens) - 1:
                self.current_screen = 0
                game_state_manager.state = game_state_manager.states["Menu"]
    def draw(self,screen):
        screen.blit(self.screens[self.current_screen][self.current_frame[0]][0],(0,0))
        #Mouse
        if self.mouse_pos:
            self.pointer_rect.centerx = self.mouse_pos[0]
            self.pointer_rect.centery = self.mouse_pos[1]
            self.pointer_current_frame = animation(self.pointer_animation,self.pointer_current_frame)
            screen.blit(self.pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))
        

        

        



