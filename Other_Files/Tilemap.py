from General_Functions import *

class Tilemap():
    """
    Stores tiles, backgrounds and level data
    """
    def __init__(self):
        self.level_name = ""
        self.level_name_animation = [[None,5],[None,5],[None,5]]
        self.level_name_current_frame = [0,0]
        self.tile_width, self.tile_height = 32, 32
        self.level_data_list = []
        self.tile_rect_dict = {}
        self.slope_mask_list = []
        self.level_width = None
        self.level_height = None
        self.tile_surface = pygame.Surface((0,0))
        self.back_tile_surface = pygame.Surface((0,0))
        self.goal_animation = [
                                [pygame.image.load("Images/Tilesets/goal_1.png").convert_alpha(),5],
                                [pygame.image.load("Images/Tilesets/goal_2.png").convert_alpha(),5],
                                [pygame.image.load("Images/Tilesets/goal_3.png").convert_alpha(),5],
                              ]
        self.goal_current_frame = [0,0]
        self.goal_off_image = pygame.image.load("Images/Tilesets/goal_off.png").convert_alpha() 
        #Backgrounds 
        self.background_dict = {
            None:{
                "image":pygame.Surface((0,0),pygame.SRCALPHA),
                "start_x":0,
                "start_y":0,
                "y_offset":0,
                "lag":0,
                "length":0,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
            "level_1_background_1":{
                "image":pygame.image.load("Images/Backgrounds/level_1_background_1.png").convert(),
                "start_x":0,
                "start_y":0,
                "x_offset":0,
                "y_offset":0,
                "lag":0,
                "length":1024},
            "level_1_background_2":{
                "image":pygame.image.load("Images/Backgrounds/level_1_background_2.png").convert_alpha(),
                "start_x":0,
                "start_y":0,
                "y_offset":0,
                "lag":0.25,
                "length":1024,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
            "level_1_background_3":{
                "image":pygame.image.load("Images/Backgrounds/level_1_background_3.png").convert_alpha(),
                "start_x":0,
                "start_y":0,
                "y_offset":0,
                "lag":0.5,
                "length":1024,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
            "level_1_bottom":{
                "image":pygame.image.load("Images/Backgrounds/level_1_bottom.png").convert_alpha(),
                "start_x":0,
                "start_y":0,
                "y_offset":0,
                "lag":2,
                "length":1024,
                "x_offset_1":0,
                "x_offset_2":0,
                "x_offset_multiplier":0},
            }
        self.background_layer_1 = self.background_dict["level_1_background_1"]
        self.background_layer_2 = self.background_dict["level_1_background_2"]
        self.background_layer_3 = self.background_dict["level_1_background_3"]
        self.bottom_layer = None #Appears at bottom of level so you can't see bottom of backgrounds
    #Updates everything in the level
    def update(self,camera):
        #Backgrounds
        #Layer 1
        self.background_layer_1["x_offset"] = 0
        self.background_layer_1["y_offset"] = 0
        #Layer 2
        self.background_layer_2["x_offset_1"] = round((-camera.x)*self.background_layer_2["lag"]) + (self.background_layer_2["x_offset_multiplier"] * self.background_layer_2["length"]) + self.background_layer_2["start_x"]
        self.background_layer_2["x_offset_2"] = (round((-camera.x)*self.background_layer_2["lag"]) + self.background_layer_2["length"]) + (self.background_layer_2["x_offset_multiplier"] * self.background_layer_2["length"]) + self.background_layer_2["start_x"]
        if self.background_layer_2["x_offset_1"] <= -self.background_layer_2["length"]:
            self.background_layer_2["x_offset_multiplier"] += 1
        elif self.background_layer_2["x_offset_2"] >= self.background_layer_2["length"]:
            self.background_layer_2["x_offset_multiplier"] -= 1
        self.background_layer_2["y_offset"] = round((camera.start_y-camera.y)*self.background_layer_2["lag"]) + self.background_layer_2["start_y"]
        #Layer 3
        self.background_layer_3["x_offset_1"] = round((-camera.x)*self.background_layer_3["lag"]) + (self.background_layer_3["x_offset_multiplier"] * self.background_layer_3["length"]) + self.background_layer_3["start_x"]
        self.background_layer_3["x_offset_2"] = (round((-camera.x)*self.background_layer_3["lag"]) + self.background_layer_3["length"]) + (self.background_layer_3["x_offset_multiplier"] * self.background_layer_3["length"]) + self.background_layer_3["start_x"]
        if self.background_layer_3["x_offset_1"] <= -self.background_layer_3["length"]:
            self.background_layer_3["x_offset_multiplier"] += 1
        elif self.background_layer_3["x_offset_2"] >= self.background_layer_3["length"]:
            self.background_layer_3["x_offset_multiplier"] -= 1
        self.background_layer_3["y_offset"] = round((camera.start_y-camera.y)*self.background_layer_3["lag"]) + self.background_layer_3["start_y"]
        #Bottom
        self.bottom_layer["x_offset_1"] = round((-camera.x)*self.bottom_layer["lag"]) + (self.bottom_layer["x_offset_multiplier"] * self.bottom_layer["length"]) + self.bottom_layer["start_x"]
        self.bottom_layer["x_offset_2"] = (round((-camera.x)*self.bottom_layer["lag"]) + self.bottom_layer["length"]) + (self.bottom_layer["x_offset_multiplier"] * self.bottom_layer["length"]) + self.bottom_layer["start_x"]
        if self.bottom_layer["x_offset_1"] <= -self.bottom_layer["length"]:
            self.bottom_layer["x_offset_multiplier"] += 1
        elif self.bottom_layer["x_offset_2"] >= self.bottom_layer["length"]:
            self.bottom_layer["x_offset_multiplier"] -= 1
        self.bottom_layer["y_offset"] = self.bottom_layer["start_y"]
    #Draws behind player
    def draw_background(self,screen,camera):
        screen.blit(self.background_layer_1["image"],(self.background_layer_1["x_offset"],self.background_layer_1["y_offset"]))
        screen.blit(self.background_layer_2["image"],(self.background_layer_2["x_offset_1"],self.background_layer_2["y_offset"]))
        screen.blit(self.background_layer_2["image"],(self.background_layer_2["x_offset_2"],self.background_layer_2["y_offset"]))
        screen.blit(self.background_layer_3["image"],(self.background_layer_3["x_offset_1"],self.background_layer_3["y_offset"]))
        screen.blit(self.background_layer_3["image"],(self.background_layer_3["x_offset_2"],self.background_layer_3["y_offset"]))
        
        screen.blit(self.back_tile_surface,(0-camera.x,0-camera.y))
    def draw_goal(self,screen,all_enemies_dead,camera):
        if all_enemies_dead:
            self.goal_current_frame = animation(self.goal_animation,self.goal_current_frame)
            goal_image = self.goal_animation[self.goal_current_frame[0]][0]
        else:
            goal_image = self.goal_off_image
            self.goal_current_frame = [0,0]
        for goal in self.tile_rect_dict["goal_rect_dict"].keys():
            #The key of a goal is a rect in tuple form
            screen.blit(goal_image,(goal[0]-camera.x,goal[1]-camera.y))
    #Draws in front of player
    def draw(self,screen,camera):
        screen.blit(self.tile_surface,(0-camera.x,0-camera.y))
        screen.blit(self.bottom_layer["image"],(self.bottom_layer["x_offset_1"],self.bottom_layer["y_offset"]-camera.y))
        screen.blit(self.bottom_layer["image"],(self.bottom_layer["x_offset_2"],self.bottom_layer["y_offset"]-camera.y))
        self.level_name_current_frame = animation(self.level_name_animation,self.level_name_current_frame)
    def draw_ui(self,screen,camera):
        screen.blit(self.level_name_animation[self.level_name_current_frame[0]][0],(864,0))
    def set_background_start_positions(self,camera_start_x,camera_start_y):
        self.background_layer_2["start_x"] = camera_start_x  
        self.background_layer_2["start_y"] = 576 - self.background_layer_2["image"].get_rect().height
        self.background_layer_3["start_x"] = camera_start_x  
        self.background_layer_3["start_y"] = 576 - self.background_layer_3["image"].get_rect().height
        self.bottom_layer["start_x"] = camera_start_x  
        self.bottom_layer["start_y"] = self.level_height - self.bottom_layer["image"].get_rect().height