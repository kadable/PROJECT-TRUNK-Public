from General_Functions import *

"""
Manages adding, updating and drawing bullets.
Used for both player and enemy bullets.
"""

class Bullets():
    def __init__(self,player=False):
        self.player = player #Player bullets can't go through grates
        self.reset()
    def add_bullet(self,bullet_centerx,bullet_centery,bullet_dir,bullet_rect_width,bullet_rect_height,bullet_mask,bullet_speed,bullet_decay,bullet_animation,bullet_damage = 1):
        bullet_speed = clamp(bullet_speed,-15,15) #Sheild rect
        bullet = {
            "x":0,
            "y":0,
            "rect":pygame.Rect(0,0,bullet_rect_width,bullet_rect_height),
            "mask":bullet_mask,
            "dir":bullet_dir,
            "speed":bullet_speed,
            "decay":bullet_decay,
            "damage":bullet_damage,
            "animation":bullet_animation,
            "current_frame":[0,0],
        }
        bullet["rect"].center = (bullet_centerx,bullet_centery)
        bullet["x"] = bullet["rect"].x
        bullet["y"]= bullet["rect"].y
        self.bullet_list.append(bullet)
    def add_lobber(self,bullet_centerx,bullet_centery,bullet_dir,bullet_rect_width,bullet_rect_height,bullet_mask,bullet_speed,bullet_grv,bullet_decay,bullet_animation,bullet_damage = 1):
        bullet_speed = clamp(bullet_speed,-15,15) #Sheild rect
        bullet = {
            "x":0,
            "y":0,
            "rect":pygame.Rect(0,0,bullet_rect_width,bullet_rect_height),
            "mask":bullet_mask,
            "dir":bullet_dir,
            "speed":bullet_speed,
            "grv":bullet_grv,
            "decay":bullet_decay,
            "damage":bullet_damage,
            "animation":bullet_animation,
            "current_frame":[0,0]
        }
        bullet["rect"].center = (bullet_centerx,bullet_centery)
        bullet["x"] = bullet["rect"].x
        bullet["y"]= bullet["rect"].y
        self.lobber_list.append(bullet)
    def add_wavy_bullet(self,bullet_centerx,bullet_centery,bullet_dir,bullet_x_stretch,bullet_y_stretch,bullet_rect_width,bullet_rect_height,bullet_mask,bullet_speed,bullet_decay,bullet_animation,bullet_damage = 1):
        bullet_speed = clamp(bullet_speed,-15,15) #Sheild rect
        bullet = {
            "start_x":bullet_centerx,
            "x":0,
            "start_y":bullet_centery,
            "y":0,
            "rect":pygame.Rect(0,0,bullet_rect_width,bullet_rect_height),
            "mask":bullet_mask,
            "dir":bullet_dir,
            "x_stretch":bullet_x_stretch,
            "y_stretch":bullet_y_stretch,
            "speed":bullet_speed,
            "decay":bullet_decay,
            "damage":bullet_damage,
            "animation":bullet_animation,
            "current_frame":[0,0],
        }
        bullet["rect"].center = (bullet_centerx,bullet_centery)
        bullet["x"] = bullet["rect"].x
        bullet["y"]= bullet["rect"].y
        self.wavy_bullet_list.append(bullet)    
    def update(self,tilemap):
        if self.player:
            self.tile_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] + tilemap.tile_rect_dict["enemy_solid_rect_list"] + tilemap.tile_rect_dict["bullet_solid_rect_list"]
        else:
            self.tile_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] + tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.slope_mask_list = tilemap.slope_mask_list
        bullet_index = 0
        #Normal Bullets
        for bullet in self.bullet_list[:]:
            #Solid Collision
            if bullet["rect"].collidelistall(self.tile_rect_list):
                self.bullet_list.remove(bullet)
                continue
            #Slope Collision
            slope_collision = False
            all_slope_collision_checks = bullet["rect"].collidelistall(self.slope_rect_list)
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                slope_offset_x = round(mask_data[1] - bullet["x"])
                slope_offset_y = round(mask_data[2] - bullet["y"])
                if bullet["mask"].overlap(mask_data[0],(slope_offset_x,slope_offset_y)):
                    slope_collision = True
                    break
            if slope_collision == True:
                self.bullet_list.remove(bullet)
                continue
            self.bullet_list[bullet_index]["decay"] -= 1
            #First becomes decayed
            if self.bullet_list[bullet_index]["decay"] <= 0 and self.bullet_list[bullet_index]["animation"] != self.bullet_decay_animation:
                self.decay_bullet(self.bullet_list,bullet_index,True)
            #When decay animation is finished
            if self.bullet_list[bullet_index]["decay"] <= 0:
                if self.bullet_list[bullet_index]["current_frame"][0] >= len(self.bullet_list[bullet_index]["animation"])-1 and self.bullet_list[bullet_index]["animation"] == self.bullet_decay_animation:
                    self.bullet_list.remove(bullet)
                    continue
            self.bullet_list[bullet_index]["x"] += round(self.bullet_list[bullet_index]["dir"][0] * self.bullet_list[bullet_index]["speed"],2)
            self.bullet_list[bullet_index]["y"] += round(self.bullet_list[bullet_index]["dir"][1] * self.bullet_list[bullet_index]["speed"],2)
            self.bullet_list[bullet_index]["rect"].x = self.bullet_list[bullet_index]["x"]
            self.bullet_list[bullet_index]["rect"].y = self.bullet_list[bullet_index]["y"]
            bullet_index += 1
        #Lobbers
        bullet_index = 0
        for bullet in self.lobber_list[:]:
            #Solid Collision
            if bullet["rect"].collidelistall(self.tile_rect_list):
                self.lobber_list.remove(bullet)
                continue
            #Slope Collision
            slope_collision = False
            all_slope_collision_checks = bullet["rect"].collidelistall(self.slope_rect_list)
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                slope_offset_x = round(mask_data[1] - bullet["x"])
                slope_offset_y = round(mask_data[2] - bullet["y"])
                if bullet["mask"].overlap(mask_data[0],(slope_offset_x,slope_offset_y)):
                    slope_collision = True
                    break
            if slope_collision == True:
                self.lobber_list.remove(bullet)
                continue
            self.lobber_list[bullet_index]["decay"] -= 1
            #First becomes decayed
            if self.lobber_list[bullet_index]["decay"] <= 0 and self.lobber_list[bullet_index]["animation"] != self.bullet_decay_animation:
                self.decay_bullet(self.lobber_list,bullet_index,True)
            #When decay animation is finished
            if self.lobber_list[bullet_index]["decay"] <= 0:
                if self.lobber_list[bullet_index]["current_frame"][0] >= len(self.lobber_list[bullet_index]["animation"])-1 and self.lobber_list[bullet_index]["animation"] == self.bullet_decay_animation:
                    self.lobber_list.remove(bullet)
                    continue
            self.lobber_list[bullet_index]["x"] += round(self.lobber_list[bullet_index]["dir"][0] * self.lobber_list[bullet_index]["speed"],2)
            self.lobber_list[bullet_index]["dir"][1] += self.lobber_list[bullet_index]["grv"]
            self.lobber_list[bullet_index]["y"] += round(self.lobber_list[bullet_index]["dir"][1] * self.lobber_list[bullet_index]["speed"],2)
            self.lobber_list[bullet_index]["rect"].x = self.lobber_list[bullet_index]["x"]
            self.lobber_list[bullet_index]["rect"].y = self.lobber_list[bullet_index]["y"]
            bullet_index += 1
        #Wavy Bullets
        tile_rect_list_for_wavy_bullets =  tilemap.tile_rect_dict["enemy_solid_rect_list"] 
        bullet_index = 0
        #Solid Collision
        for bullet in self.wavy_bullet_list[:]:
            if bullet["rect"].collidelistall(tile_rect_list_for_wavy_bullets):
                self.wavy_bullet_list.remove(bullet)
                continue
            self.wavy_bullet_list[bullet_index]["decay"] -= 1
            #First becomes decayed
            if self.wavy_bullet_list[bullet_index]["decay"] <= 0 and self.wavy_bullet_list[bullet_index]["animation"] != self.bullet_decay_animation:
                self.decay_bullet(self.wavy_bullet_list,bullet_index,True)
            #When decay animation is finished
            if self.wavy_bullet_list[bullet_index]["decay"] <= 0:
                if self.wavy_bullet_list[bullet_index]["current_frame"][0] >= len(self.wavy_bullet_list[bullet_index]["animation"])-1 and self.wavy_bullet_list[bullet_index]["animation"] == self.bullet_decay_animation:
                    self.wavy_bullet_list.remove(bullet)
                    continue
            self.wavy_bullet_list[bullet_index]["x"] += round(self.wavy_bullet_list[bullet_index]["dir"][0] * self.wavy_bullet_list[bullet_index]["speed"],2)
            self.wavy_bullet_list[bullet_index]["y"] = self.wavy_bullet_list[bullet_index]["start_y"] + round(self.wavy_bullet_list[bullet_index]["dir"][1] * self.wavy_bullet_list[bullet_index]["y_stretch"] * math.sin((self.wavy_bullet_list[bullet_index]["x"] - self.wavy_bullet_list[bullet_index]["start_x"]) * self.wavy_bullet_list[bullet_index]["x_stretch"]),2)
            self.wavy_bullet_list[bullet_index]["rect"].x = self.wavy_bullet_list[bullet_index]["x"]
            self.wavy_bullet_list[bullet_index]["rect"].y = self.wavy_bullet_list[bullet_index]["y"]
            bullet_index += 1
    def draw(self,screen,camera):
        draw_list = self.bullet_list.copy() + self.lobber_list.copy() + self.wavy_bullet_list.copy()
        for bullet in draw_list:
            bullet["current_frame"] = animation(bullet["animation"],bullet["current_frame"])
            bullet_image = bullet["animation"][bullet["current_frame"][0]][0]
            bullet_image_rect = bullet_image.get_rect()
            if bullet["decay"] <= 0:
                #Needed as rect when a bullet is decayed has 0 width and height
                bullet_image_rect.center = bullet["decay_draw_rect"].center
            else:
                bullet_image_rect.center = bullet["rect"].center
            screen.blit(bullet_image,(bullet_image_rect.x-camera.x,bullet_image_rect.y-camera.y))       
    def decay_bullet(self,bullet_list,bullet_index,decay_animation= False):
        if decay_animation:
            bullet_list[bullet_index]["animation"] = self.bullet_decay_animation
            bullet_list[bullet_index]["current_frame"] = [0,0]
            bullet_list[bullet_index]["decay_draw_rect"] = bullet_list[bullet_index]["rect"].copy()
            bullet_list[bullet_index]["rect"].width = 0
            bullet_list[bullet_index]["rect"].height = 0
            bullet_list[bullet_index]["speed"] = 0
        else:
            bullet_list.pop(bullet_index)
    def reset(self):
        self.bullet_list = []
        self.lobber_list = []
        self.wavy_bullet_list = []
        #Animations
        self.bullet_decay_animation = [[pygame.image.load("Images/Bullets/bullet_decay_animation_1.png"),1],
                                       [pygame.image.load("Images/Bullets/bullet_decay_animation_2.png"),1],
                                       [pygame.image.load("Images/Bullets/bullet_decay_animation_3.png"),1],
                                       [pygame.image.load("Images/Bullets/bullet_decay_animation_4.png"),1],
                                       [pygame.image.load("Images/Bullets/bullet_decay_animation_5.png"),1],
                                      ]
        #Collision Lists
        self.tile_rect_list = []
        self.slope_rect_list = []
        self.slope_mask_list = []
        self.bullet_solid_rect_list = []
        



