from General_Functions import *
from Enemies import *

class Instances():
    """
    Manages adding to level, updating and drawing instances.
    Just enemies in the engine but could be more in future.
    """
    def __init__(self):
        self.instance_dict = {}
        #So it knows what class to add when Game_State_Manager (which doesn't have Enemy imported) 
        #says add an Enemy
        self.add_instance_dict = {
                                   "Monobrow_Bug":Monobrow_Bug,
                                   "Mouth_Stack":Mouth_Stack,
                                   "Beak_Balloon":Beak_Balloon,
                                   "Jaw_Cloud":Jaw_Cloud,
                                   "Cyclops_Turret":Cyclops_Turret,
                                   "Donut":Donut,
                                   "Winged_Donut":Winged_Donut,
                                   "Snout_Slime":Snout_Slime,
                                   "Slug_Bug":Slug_Bug,
                                   "Tap_Bug":Tap_Bug,
                                   "Villiform_Man":Villiform_Man,
                                   "flower":Flower,
                                   "grass":Grass,
                                   "fence":Fence,
                                   "fence_stump":Fence_Stump,
                                   "cave":Cave,
                                   "big_cave":Big_Cave,
                                   "bush":Bush,
                                   "vine":Vine,
                                   "vine_flower":Vine_Flower,
                                   "mushroom":Mushroom,
                                   }
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        for enemy in self.instance_dict["enemy_list"]:
            enemy.update(tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector)
        for decor in self.instance_dict["decor_list"]:
           decor.update()
        for decor in self.instance_dict["decor_behind_list"]:
           decor.update()
    #Draw behind player
    def draw_behind(self,screen,camera):
        for decor in self.instance_dict["decor_behind_list"]:
            decor.draw(screen,camera)
    def draw(self,screen,camera):
        for enemy in self.instance_dict["enemy_list"]:
            enemy.draw(screen,camera)
        for decor in self.instance_dict["decor_list"]:
            decor.draw(screen,camera)
    def add_instance(self,instance_dict_key,instance_class_name,x,y):
        self.instance_dict[instance_dict_key].append(self.add_instance_dict[instance_class_name](x,y))
    def bounce_screen_shake_check(self):
        for enemy in self.instance_dict["enemy_list"]:
            if enemy.bounce_screen_shake_timer > 0:
                return True
        return False
    def reset(self):
        for enemy in self.instance_dict["enemy_list"]:
            enemy.reset()

class Decor():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.animation = []
        self.current_frame = [0,0]
    def update(self):
        self.current_frame = animation(self.animation,self.current_frame)
    def draw(self,screen,camera):
        screen.blit(self.animation[self.current_frame[0]][0],(self.x-camera.x,self.y-camera.y))

class Flower(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/flower_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/flower_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/flower_3.png").convert_alpha(),5]
                        ]
        self.current_frame[1] = random.randint(1,9)

class Grass(Flower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/grass_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/grass_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/grass_3.png").convert_alpha(),5]
                        ]

class Fence(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/fence_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/fence_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/fence_3.png").convert_alpha(),5],
                        ]
        self.current_frame[1] = random.randint(1,9)

class Fence_Stump(Fence):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/fence_stump_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/fence_stump_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/fence_stump_3.png").convert_alpha(),5]
                        ]

class Cave(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/cave.png").convert_alpha(),5],
                        ]

class Big_Cave(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/big_cave.png").convert_alpha(),5],
                        ]
    def draw(self,screen,camera):
        screen.blit(self.animation[self.current_frame[0]][0],(self.x-32-camera.x,self.y-32-camera.y))

class Bush(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/bush_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/bush_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/bush_3.png").convert_alpha(),5]
                        ]
        self.current_frame[1] = random.randint(1,9)

class Vine(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/vine_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/vine_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/vine_3.png").convert_alpha(),5]
                        ]
        self.current_frame[1] = random.randint(1,9)
        
class Vine_Flower(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/vine_flower_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/vine_flower_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/vine_flower_3.png").convert_alpha(),5]
                        ]
        self.current_frame[1] = random.randint(1,9)

class Mushroom(Decor):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.animation = [[pygame.image.load("Images/Decor/mushroom_1.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/mushroom_2.png").convert_alpha(),5],
                          [pygame.image.load("Images/Decor/mushroom_3.png").convert_alpha(),5]
                        ]
        self.current_frame[1] = random.randint(1,9)
    def draw(self,screen,camera):
        screen.blit(self.animation[self.current_frame[0]][0],(self.x-camera.x,self.y-32-camera.y))
