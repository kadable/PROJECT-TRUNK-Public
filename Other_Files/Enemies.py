from General_Functions import *
from Bullets import *

#All enemies should inherit from this class
class Enemy(): 
    def __init__(self,x,y):
        self.start_x = x
        self.start_y = y
        self.reset()
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Bounce Screen Shake
        if self.bounce_screen_shake_timer > 0:
            self.bounce_screen_shake_timer -= 1
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["jump_through_platform_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] +  tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        self.player_aiming_vector = player_aiming_vector 
        if player_sheild_data[0]:
            self.player_sheild_rect = player_sheild_data[1]
        else:
            self.player_sheild_rect = pygame.Rect(0,0,0,0)
        #Normal
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        else:
            self.state[1](player_bullets) #Needs as it needs to delete player bullets if dead
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            screen.blit(self.image,(self.x-camera.x,self.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def start_normal(self):
        pass
    def normal(self,player_bullets):
        pass
    def dead_start(self):
        self.x,self.y = self.rect.center
        print("1",self.x,self.y)
        self.rect = (0,0,0,0)
        print("2",self.x,self.y)
        self.animation,self.current_frame = switch_animation(self.animation,self.death_animation,self.current_frame)
    def dead(self):
        #Dead state instead of deleting enemy allows for much easier restarting of level
        pass
    def player_bullet_collision(self,player_bullets):
        player_bullet_index = 0
        for bullet in self.player_bullet_list:
            if self.rect.colliderect(bullet["rect"]):
                self.health -= player_bullets.bullet_list[player_bullet_index]["damage"]
                #player_bullets.bullet_list[player_bullet_index]["decay"] = 0
                player_bullets.decay_bullet(player_bullets.bullet_list,player_bullet_index)
                self.hurt_flash_timer = 0
                if self.health <= 0:
                    self.next_state = self.states["Dead"]
                    return
            player_bullet_index += 1
    def reset(self):
        #States
        self.states = {"Normal":[self.start_normal,self.normal],"Dead":[self.dead_start,self.dead]}
        self.state = self.states["Normal"]
        self.next_state = self.states["Normal"]
        #General Attributes
        self.x = self.start_x
        self.y = self.start_y
        self.hsp = 0
        self.vsp = 0
        self.image = pygame.image.load("Images/Enemies/enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.health = 0
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/enemy.png").convert_alpha(),10]]
        self.death_animation = [[pygame.image.load("Images/Enemies/enemy_death_1.png").convert_alpha(),3],
                                [pygame.image.load("Images/Enemies/enemy_death_2.png").convert_alpha(),3],
                                [pygame.image.load("Images/Enemies/enemy_death_3.png").convert_alpha(),3],
                                [pygame.image.load("Images/Enemies/enemy_death_4.png").convert_alpha(),3],
                                [pygame.image.load("Images/Enemies/enemy_death_5.png").convert_alpha(),3],
                               ]
        self.animation = self.normal_animation
        self.current_frame = [0,0]
        self.hurt_flash_max = 7
        self.hurt_flash_timer = self.hurt_flash_max
        #Collision Lists
        self.player_bullet_list = None
        self.player_sheild_rect = None
        #Tiles
        self.solid_rect_list = []
        self.slope_rect_list = []
        #Bullets
        self.player_bullet_list = []
        #Normal State
        self.player_aiming_vector = None
        self.bounce_screen_shake_timer = 0
        self.bounce_screen_shake_max = 5  

class Monobrow_Bug(Enemy):
    """
    Simple guy, moves back and forth, encourages jumping
    """
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.centerx = self.rect.centerx
            draw_rect.bottom = self.rect.bottom
            if self.dir > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,player_bullets):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            cliff_check_rect = self.rect.move(sign(self.hsp)*self.rect.width,1)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list)\
            or not cliff_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/monobrow_bug_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/monobrow_bug_hitbox.png").get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.dir = 1
        self.health = 8
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/monobrow_bug_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/monobrow_bug_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/monobrow_bug_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Normal State
        self.normal_speed = 2
    
class Shooting_Enemy(Enemy):
    """
    Every shooting enemy inherits from here
    """
    def __init__(self,x,y):
        super().__init__(x,y)
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Bounce Screen Shake
        if self.bounce_screen_shake_timer > 0:
            self.bounce_screen_shake_timer -= 1
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["jump_through_platform_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] +  tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        self.player_aiming_vector = player_aiming_vector 
        if player_sheild_data[0]:
            self.player_sheild_rect = player_sheild_data[1]
        else:
            self.player_sheild_rect = pygame.Rect(0,0,0,0)
        #Normal
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        else:
            self.state[1](enemy_bullets,player_bullets) #Needs as it needs to delete player bullets if dead
    def normal(self,enemy_bullets,player_bullets):
        pass
    def reset(self):
        super().reset()
        self.bullet_animation = [[pygame.image.load("Images/Bullets/enemy_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_3.png").convert_alpha(),5]]
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 12
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_bullet_1.png"))

class Beak_Balloon(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Bounce Screen Shake
        if self.bounce_screen_shake_timer > 0:
            self.bounce_screen_shake_timer -= 1
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] +  tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        if player_sheild_data[0]:
            self.player_sheild_rect = player_sheild_data[1]
        else:
            self.player_sheild_rect = pygame.Rect(0,0,0,0)
        self.player_aiming_vector = player_aiming_vector
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        elif self.state == self.states["Normal"]:
            self.state[1](player_bullets,player_x,player_y)
        else:
            self.state[1](player_bullets) #Needs as it needs to delete player bullets if dead
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_x = self.x
            if self.dir[0] < 0:
                self.image = pygame.transform.flip(self.image, True, False)
                draw_x -= self.draw_offset #Compensate for beak which isn't part of hitbox
            #pygame.draw.rect(screen,(0,255,0),self.rect)
            screen.blit(self.image,(draw_x-camera.x,self.y-camera.y))
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def start_normal(self):
        #self.normal_speed_x = 0
        #self.normal_speed_y = 0
        pass
    def normal(self,player_bullets,player_x,player_y):
        #Targeting Player
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector  
        #Can't normalise vector 0
        if (self.target_vector.length() > self.range and self.aggro == False) or self.target_vector.length() == 0:
            self.dir = [0,0]
        elif self.target_vector.length() > self.range/2: #Swoops down
            player_vector = pygame.math.Vector2(player_x,player_y+40)
            self.target_vector = player_vector - enemy_vector  
            if self.target_vector.length() == 0:
                self.dir = [0,0]
            else:
                self.target_vector = self.target_vector.normalize()
                self.dir = [self.target_vector.x,self.target_vector.y]
            self.aggro = True
        else:
            player_vector = pygame.math.Vector2(player_x,player_y-40)
            self.target_vector = player_vector - enemy_vector  
            if self.target_vector.length() == 0:
                self.dir = [0,0]
            else:
                self.target_vector = self.target_vector.normalize()
                self.dir = [self.target_vector.x,self.target_vector.y]
            self.aggro = True
        if sign(self.normal_speed_x) != sign(self.dir[0]):
            acceleration = self.normal_decceleration
        else:
            acceleration = self.normal_acceleration
        self.normal_speed_x = self.normal_speed_x + (acceleration * self.dir[0])
        self.normal_speed_x = clamp(self.normal_speed_x,-self.normal_speed_max,self.normal_speed_max)
        if sign(self.normal_speed_y) != sign(self.dir[1]):
            acceleration = self.normal_decceleration
        else:
            acceleration = self.normal_acceleration
        self.normal_speed_y = self.normal_speed_y + (acceleration * self.dir[1])
        self.normal_speed_y = clamp(self.normal_speed_y,-self.normal_speed_max,self.normal_speed_max) 
        self.hsp = self.normal_speed_x
        self.vsp = self.normal_speed_y
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Player sheild collision
        if self.player_sheild_rect:
            if self.rect.colliderect(self.player_sheild_rect):
                self.hsp = 0
                self.vsp = 0
                self.normal_speed_x = self.bounce_speed_max * self.player_aiming_vector.x
                self.normal_speed_y = self.bounce_speed_max * self.player_aiming_vector.y
                self.next_state = self.states["Bounce"]
                return
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            #Player sheild collision
            if self.player_sheild_rect:
                if collision_check_rect.colliderect(self.player_sheild_rect):
                    self.hsp = 0
                    self.vsp = 0
                    self.normal_speed_x = self.bounce_speed_max * self.player_aiming_vector.x
                    self.normal_speed_y = self.bounce_speed_max * self.player_aiming_vector.y
                    self.next_state = self.states["Bounce"]
                    return
            #Tile Collision
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list):
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
        for i in range(math.ceil(abs(self.vsp))):
            #Player sheild collision
            if self.player_sheild_rect:
                if self.rect.colliderect(self.player_sheild_rect):
                    self.hsp = 0
                    self.vsp = 0
                    self.normal_speed_x = self.bounce_speed_max * self.player_aiming_vector.x
                    self.normal_speed_y = self.bounce_speed_max * self.player_aiming_vector.y
                    self.next_state = self.states["Bounce"]
                    return
            #Tile Collision
            collision_check_rect = self.rect.move(0,sign(self.vsp))
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list):
                break
            else:
                self.y += sign(self.vsp)
                self.rect.y = self.y
    def start_bounce(self):
        self.bounce_timer = self.bounce_max
        self.bounce_screen_shake_timer = self.bounce_screen_shake_max
    def bounce(self,player_bullets):
        self.hsp = self.normal_speed_x
        self.vsp = self.normal_speed_y
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list):
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
        for i in range(math.ceil(abs(self.vsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(0,sign(self.vsp))
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list):
                break
            else:
                self.y += sign(self.vsp)
                self.rect.y = self.y
        #Timer
        self.bounce_timer -= 1
        if self.bounce_timer <= 0:
            self.next_state = self.states["Normal"]
    def dead(self):
        #Dead state instead of deleting enemy allows for much easier restarting of level
        pass
    def reset(self):
        super().reset()
        #States
        self.states = {"Normal":[self.start_normal,self.normal],"Bounce":[self.start_bounce,self.bounce],"Dead":[self.dead_start,self.dead]}
        self.state = self.states["Normal"]
        self.next_state = self.states["Normal"]
        self.aggro = False
        #General Attributes
        self.x = self.start_x
        self.y = self.start_y
        self.hsp = 0
        self.vsp = 0
        self.image = pygame.image.load("Images/Enemies/beak_balloon_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/beak_balloon_hitbox.png").get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.dir = [0,0]
        self.health = 7
        self.target_vector = None
        #Animations
        self.draw_offset = 13
        self.normal_animation = [[pygame.image.load("Images/Enemies/beak_balloon_1.png").convert_alpha(),10],[pygame.image.load("Images/Enemies/beak_balloon_2.png").convert_alpha(),10],[pygame.image.load("Images/Enemies/beak_balloon_3.png").convert_alpha(),10]]
        self.animation = self.normal_animation
        self.current_frame = [0,0]
        self.hurt_flash_max = 7
        self.hurt_flash_timer = self.hurt_flash_max
        #Bullets
        self.player_bullet_list = []
        #Normal State
        self.normal_speed_x = 0
        self.normal_speed_y = 0
        self.normal_speed_max = 3
        self.normal_acceleration = 0.1
        self.normal_decceleration = 0.25
        self.range = 400
        #Bounce State
        self.bounce_speed_max = 5
        self.player_aiming_vector = None
        self.bounce_max = 25
        self.bounce_timer = self.bounce_max
        self.bounce_screen_shake_timer = 0
        self.bounce_screen_shake_max = 5        

class Jaw_Cloud(Beak_Balloon):
    """
    Flies towards player with no acceleration
    """
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center 
            if self.dir[0] < 0:
                self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/jaw_cloud_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/jaw_cloud_hitbox.png").get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.health = 12
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/jaw_cloud_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/jaw_cloud_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/jaw_cloud_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Normal State
        self.normal_speed_max = 2.3
        self.normal_acceleration = 0.3
        self.normal_decceleration = 0.32
        self.range = 400
        #Bounce State
        self.bounce_max = 20
        self.bounce_speed_max = 5

class Cyclops_Turret(Shooting_Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            if sign(self.target_vector.x) > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["jump_through_platform_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] +  tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        #Normal
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        else:
            self.state[1](enemy_bullets,player_bullets,player_x,player_y) #Needs as it needs to delete player bullets if dead
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector 
        if self.target_vector.length() == 0:
            self.dir = [1,0]
        elif self.target_vector.length() <= self.range:
            self.target_vector = self.target_vector.normalize()
            self.dir = [self.target_vector.x,self.target_vector.y]
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        if self.target_vector.length() <= self.range:
            self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.target_vector.length() <= self.range:
            self.shoot_bullet_timer = 0
            enemy_bullets.add_bullet(self.rect.centerx,self.rect.centery-25,[self.dir[0],self.dir[1]],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        self.image = pygame.image.load("Images/Enemies/cyclops_turret_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/cyclops_turret_hitbox.png").get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.dir = [1,0]
        self.health = 10
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/cyclops_turret_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/cyclops_turret_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/cyclops_turret_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        self.current_frame = [0,0]
        #Shooting
        self.target_vector = pygame.math.Vector2(0,0)
        self.shoot_bullet_timer = random.randint(0,80)
        self.shoot_bullet_max = 80
        self.bullet_dir = [1,0]
        self.bullet_speed = 3
        self.bullet_decay = 200 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 12
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_bullet_1.png"))
        #Normal State
        self.normal_speed = 2
        self.range = 400

class Donut(Shooting_Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center 
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)    
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Shoot bullets
        self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max:
            self.shoot_bullet_timer = 0 + random.randint(-5,5)
            enemy_bullets.add_bullet(self.rect.centerx,self.rect.bottom,self.bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/donut_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/donut_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.health = 10
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/donut_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/donut_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/donut_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Shooting
        #[x,y,rect,[dir_x,dir_y],speed,decay]
        self.bullet_animation = self.bullet_animation = [[pygame.image.load("Images/Bullets/winged_donut_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = random.randint(0,49)
        self.shoot_bullet_max = 42
        self.bullet_dir = [0,1]
        self.bullet_speed = 2
        self.bullet_decay = 200 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 36
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/winged_donut_bullet_1.png"))
        #Normal State
        self.normal_speed = 2
        
class Mouth_Stack(Cyclops_Turret):
    """
    Moves back and forth, shoots a column of three bullets (can't all be blocked, encourages jumping)
    """
    def __init__(self,x,y):
        super().__init__(x,y)
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Bounce Screen Shake
        if self.bounce_screen_shake_timer > 0:
            self.bounce_screen_shake_timer -= 1
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["jump_through_platform_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] + tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        self.player_aiming_vector = player_aiming_vector 
        if player_sheild_data[0]:
            self.player_sheild_rect = player_sheild_data[1]
        else:
            self.player_sheild_rect = pygame.Rect(0,0,0,0)
        #Normal
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        else:
            self.state[1](enemy_bullets,player_bullets,player_x,player_y) #Needs as it needs to delete player bullets if dead
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            if sign(self.target_vector.x) < 0:
                self.image = pygame.transform.flip(self.image, True, False)
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            cliff_check_rect = self.rect.move(sign(self.hsp)*self.rect.width,1)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list)\
            or not cliff_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Work out target vectors
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector 
        
        """
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector 
        if self.target_vector.length() == 0:
            self.dir = [1,0]
        elif self.target_vector.length() <= self.range:
            self.target_vector = self.target_vector.normalize()
            self.dir = [self.target_vector.x,self.target_vector.y]
        """
        #Shoot bullets
        if self.target_vector.length() <= self.range: 
            self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.target_vector.length() <= self.range and self.target_vector.length() != 0 :
            self.shoot_bullet_timer = 0
            bullet_dir = [sign(self.target_vector.x),0]
            if self.shooting_state == 1:
                enemy_vector = pygame.math.Vector2(self.x+20,self.y+20)
                player_vector = pygame.math.Vector2(player_x,player_y-50)
                self.target_vector = player_vector - enemy_vector 
                bullet_dir = [self.target_vector.normalize().x,self.target_vector.normalize().y]
                enemy_bullets.add_bullet(self.rect.centerx,self.y+20,bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
                enemy_vector = pygame.math.Vector2(self.x+110,self.y+110)
                player_vector = pygame.math.Vector2(player_x,player_y+50)
                self.target_vector = player_vector - enemy_vector 
                bullet_dir = [self.target_vector.normalize().x,self.target_vector.normalize().y]
                enemy_bullets.add_bullet(self.rect.centerx,self.y+110,bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
                self.shooting_state = 2
            else:
                enemy_vector = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
                player_vector = pygame.math.Vector2(player_x,player_y)
                self.target_vector = player_vector - enemy_vector 
                bullet_dir = [self.target_vector.normalize().x,self.target_vector.normalize().y]
                enemy_bullets.add_bullet(self.rect.centerx,self.rect.centery,bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
                self.shooting_state = 1
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/mouth_stack_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/mouth_stack_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.health = 20
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/mouth_stack_1.png").convert_alpha(),2],[pygame.image.load("Images/Enemies/mouth_stack_2.png").convert_alpha(),2],[pygame.image.load("Images/Enemies/mouth_stack_3.png").convert_alpha(),2]]
        self.animation = self.normal_animation
        #Normal
        self.normal_speed = 0.25
        self.range = 600
        #Shooting
        self.target_vector = pygame.math.Vector2(0,0)
        self.shooting_state = 1 #1 or 2
        self.bullet_animation = [[pygame.image.load("Images/Bullets/enemy_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = 0
        self.shoot_bullet_max = 55
        self.bullet_speed = 2.5
        self.bullet_decay = 500 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 12
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_bullet_1.png"))

class Winged_Donut(Mouth_Stack):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center 
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)    
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        enemy_vector = pygame.math.Vector2(self.rect.centerx,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector 
        if abs(self.target_vector.x) <= self.normal_range:
            self.dir = sign(self.target_vector.x)
        else:
            self.dir = 0
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Player sheild_collision
        if self.player_sheild_rect:
            if self.rect.colliderect(self.player_sheild_rect):
                if self.bounce_speed_max != 0:
                    self.hsp = self.bounce_speed_max * sign(self.player_aiming_vector.x)
                    self.next_state = self.states["Bounce"]
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list):
                self.hsp = 0
                break
            else:
                if self.rect.centerx == player_x:
                    break
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Shoot bullets
        self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max:
            self.shoot_bullet_timer = 0 + random.randint(-5,5)
            enemy_bullets.add_bullet(self.rect.centerx,self.rect.bottom,self.bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def start_bounce(self):
        self.bounce_timer = self.bounce_max
        self.bounce_screen_shake_timer = self.bounce_screen_shake_max
    def bounce(self,enemy_bullets,player_bullets,player_x,player_y):
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list):
                self.hsp = 0
                break
            else:
                if self.rect.centerx == player_x:
                    break
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Timer
        self.bounce_timer -= 1
        if self.bounce_timer <= 0:
            self.next_state = self.states["Normal"]
    def reset(self):
        super().reset()
        #States
        self.states = {"Normal":[self.start_normal,self.normal],"Bounce":[self.start_bounce,self.bounce],"Dead":[self.dead_start,self.dead]}
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/winged_donut_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/donut_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.health = 20
        #Animations
        self.normal_animation = [[pygame.image.load("Images/Enemies/winged_donut_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/winged_donut_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/winged_donut_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Shooting
        #[x,y,rect,[dir_x,dir_y],speed,decay]
        self.bullet_animation = self.bullet_animation = [[pygame.image.load("Images/Bullets/winged_donut_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = 0
        self.shoot_bullet_max = 45
        self.bullet_dir = [0,1]
        self.bullet_speed = 2
        self.bullet_decay = 200 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 36
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/winged_donut_bullet_1.png"))
        #Normal State
        self.normal_speed = 2.5
        self.normal_range = 300
        #Bounce State
        self.bounce_max = 60
        self.bounce_speed_max = 4

class Snout_Slime(Mouth_Stack):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            if sign(self.target_vector.x) < 0:
                self.image = pygame.transform.flip(self.image, True, False)
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center
            draw_rect.y -= self.draw_offset
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            cliff_check_rect = self.rect.move(sign(self.hsp)*self.rect.width,1)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list)\
            or not cliff_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Work out target vectors
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.target_vector = player_vector - enemy_vector 
        #Shoot bullets
        if self.target_vector.length() <= self.range:
            self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.target_vector.length() <= self.range:
            self.shoot_bullet_timer = 0
            self.bullet_dir = [random.uniform(0.1,0.4),-0.35]
            self.bullet_dir[0] = (sign(self.target_vector.x)*abs(self.bullet_dir[0]))
            enemy_bullets.add_lobber(self.rect.centerx,self.rect.centery,self.bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_grv,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/snout_slime_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/snout_slime_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.health = 10
        #Animations
        self.draw_offset = 12
        self.normal_animation = [[pygame.image.load("Images/Enemies/snout_slime_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/snout_slime_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/snout_slime_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Normal
        self.normal_speed = 1
        self.range = 900
        #Shooting
        self.target_vector = pygame.math.Vector2(0,0)
        self.bullet_animation = [[pygame.image.load("Images/Bullets/enemy_lobber_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_lobber_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_lobber_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = random.randint(1,40)
        self.shoot_bullet_max = 58
        self.bullet_dir = [2,-2]
        self.bullet_speed = 6.5
        self.bullet_grv = 0.005
        self.bullet_decay = 1000 #How long bullet lasts
        self.bullet_rect_width = 26 #For making bullet rect and positioning
        self.bullet_rect_height = 26
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_lobber_1.png"))

class Slug_Bug(Cyclops_Turret):
    def update(self,tilemap,enemy_bullets,player_bullets,player_x,player_y,player_sheild_data,player_aiming_vector):
        #Bounce Screen Shake
        if self.bounce_screen_shake_timer > 0:
            self.bounce_screen_shake_timer -= 1
        #Treats jump through platforms like solids
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"] + tilemap.tile_rect_dict["jump_through_platform_rect_list"] + tilemap.tile_rect_dict["hazard_rect_list"] + tilemap.tile_rect_dict["enemy_solid_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.player_bullet_list = player_bullets.bullet_list
        self.player_aiming_vector = player_aiming_vector 
        if player_sheild_data[0]:
            self.player_sheild_rect = player_sheild_data[1]
        else:
            self.player_sheild_rect = pygame.Rect(0,0,0,0)
        #Normal
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1]()
        else:
            self.state[1](enemy_bullets,player_bullets,player_x,player_y) #Needs as it needs to delete player bullets if dead
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            if sign(self.target_vector.x) > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center
            draw_rect.y -= self.draw_offset
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
            #pygame.draw.rect(screen,(0,255,0),self.rect)
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            cliff_check_rect = self.rect.move(sign(self.hsp)*self.rect.width,1)
            #Turning around
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list)\
            or not cliff_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Work out target vectors
        enemy_vector = pygame.math.Vector2(self.rect.centerx,self.rect.centery+10)
        player_vector = pygame.math.Vector2(player_x,player_y)
        target_vector = player_vector - enemy_vector 
        if target_vector.x == 0:
            pass
        else:
            self.target_vector = target_vector
        """
         enemy_vector = pygame.math.Vector2(self.x+20,self.y+20)
                player_vector = pygame.math.Vector2(player_x,player_y)
                self.target_vector = player_vector - enemy_vector 
                bullet_dir = [self.target_vector.normalize().x,self.target_vector.normalize().y]
        """
        if self.target_vector.length() <= self.range: 
            self.shoot_bullet_timer += 1
        #Shoot bullets
        if self.target_vector.length() <= self.range and self.target_vector.length() != 0:
            self.burst_bullet_timer += 1
            if (self.shooting and self.burst_bullet_timer >= self.burst_bullet_max_1) or (not self.shooting and self.burst_bullet_timer >= self.burst_bullet_max_2):
                self.shooting = not self.shooting
                self.burst_bullet_timer = 0
                self.bullet_dir = [sign(self.target_vector.x),clamp(self.target_vector.normalize().y,-1,0.5)]
            self.shoot_bullet_timer += 1
            if self.shoot_bullet_timer >= self.shoot_bullet_max and self.shooting:
                self.shoot_bullet_timer = 0
                enemy_bullets.add_bullet(self.rect.centerx,self.y+38,self.bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/slug_bug_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/slug_bug_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.health = 15
        #Animations
        self.draw_offset = 2
        self.normal_animation = [[pygame.image.load("Images/Enemies/slug_bug_1.png").convert_alpha(),5],
                                 [pygame.image.load("Images/Enemies/slug_bug_2.png").convert_alpha(),5],
                                 [pygame.image.load("Images/Enemies/slug_bug_3.png").convert_alpha(),5],
                                 [pygame.image.load("Images/Enemies/slug_bug_4.png").convert_alpha(),5]
                                ]
        self.animation = self.normal_animation
        #Normal
        self.normal_speed = 1
        self.range = 500
        #Shooting
        self.target_vector = pygame.math.Vector2(0,0)
        self.shooting_state = 1 #1 or 2
        self.bullet_animation = [[pygame.image.load("Images/Bullets/winged_donut_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/winged_donut_bullet_3.png").convert_alpha(),5]]        
        self.shoot_bullet_timer = random.randint(0,9)
        self.shoot_bullet_max = 9
        self.burst_bullet_timer = random.randint(0,100)
        self.burst_bullet_max_1 = 20 #Time shooting
        self.burst_bullet_max_2 = 110 #Time not shooting
        self.shooting = False
        self.bullet_speed = 2
        self.bullet_decay = 400 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 36
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/winged_donut_bullet_1.png"))
        self.bullet_dir = [1,0]

class Tap_Bug(Shooting_Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center 
            draw_rect.y -= self.draw_offset
            #pygame.draw.rect(screen,(0,255,0),self.rect)
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets):
        self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            #Tile Collision
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            cliff_check_rect = self.rect.move(sign(self.hsp)*self.rect.width,1)
            if collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list)\
            or not cliff_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                self.dir *= -1
                break
            elif collision_check_rect.colliderect(self.player_sheild_rect) and self.dir != sign(self.player_aiming_vector.x) and sign(self.player_aiming_vector.x) != 0:
                self.hsp = 0
                self.dir = sign(self.player_aiming_vector.x)
                self.bounce_timer = 0
                self.bounce_screen_shake_timer = self.bounce_screen_shake_max
                break
            else:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
        #Shoot bullets
        self.burst_bullet_timer += 1
        if (self.shooting and self.burst_bullet_timer >= self.burst_bullet_max_1) or (not self.shooting and self.burst_bullet_timer >= self.burst_bullet_max_2):
            self.shooting = not self.shooting
            self.burst_bullet_timer = 0
        self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.shooting:
            self.shoot_bullet_timer = 0
            enemy_bullets.add_bullet(self.rect.centerx,self.y-18,self.bullet_dir[:],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/tap_bug_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/tap_bug_hitbox.png").convert_alpha().get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.dir = 1
        self.health = 10
        #Animations
        self.draw_offset = 18
        self.normal_animation = [[pygame.image.load("Images/Enemies/tap_bug_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/tap_bug_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/tap_bug_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Normal State
        self.normal_speed = 1.5
        self.normal_range = 600
        #Shooting
        self.bullet_animation = [[pygame.image.load("Images/Bullets/enemy_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_bullet_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = 0
        self.shoot_bullet_max = 3
        self.burst_bullet_timer = random.randint(0,49)
        self.burst_bullet_max_1 = 35 #Time shooting
        self.burst_bullet_max_2 = 60 #Time not shooting
        self.shooting = True
        self.bullet_dir = [0,-1]
        self.bullet_speed = 2
        self.bullet_decay = 300 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 12
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_bullet_1.png"))

class Villiform_Man(Cyclops_Turret):
    def __init__(self,x,y):
        super().__init__(x,y)
    def draw(self,screen,camera):
        if self.state != self.states["Dead"]:
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            if self.hurt_flash_timer < self.hurt_flash_max:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
                self.hurt_flash_timer += 1
            draw_rect = self.image.get_rect()
            draw_rect.center = self.rect.center 
            if self.facing == 1:
                self.image = pygame.transform.flip(self.image, True, False)
                draw_rect.x += self.draw_offset #As hitbox is drawn at the back of the enemy
            else:
                draw_rect.x -= self.draw_offset 
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
        elif self.current_frame[0] != len(self.death_animation) - 1: #Draw death effect
            self.current_frame = animation(self.animation,self.current_frame)
            self.image = self.animation[self.current_frame[0]][0]
            draw_rect = self.image.get_rect()
            draw_rect.center = self.x,self.y
            screen.blit(self.image,(draw_rect.x-camera.x,draw_rect.y-camera.y))
    def normal(self,enemy_bullets,player_bullets,player_x,player_y):
        enemy_vector = pygame.math.Vector2(self.x,self.y)
        player_vector = pygame.math.Vector2(player_x,player_y)
        self.difference_vector = player_vector - enemy_vector 
        self.facing = sign(self.difference_vector.x)
        self.shooting_dir = sign(self.difference_vector.x)
        player_offset_x = player_x - (self.shooting_dir * self.normal_distance_from_player)
        player_offset_vector = pygame.math.Vector2(player_offset_x,player_y)
        self.target_vector = player_offset_vector - enemy_vector 
        if self.target_vector.length() > self.range:
            self.target_vector = pygame.math.Vector2(0,0)
        self.dir = sign(self.target_vector.x)
        if self.difference_vector.length() <= self.range:
            self.hsp = self.normal_speed * self.dir
        #Player bullet collision
        self.player_bullet_collision(player_bullets)
        #Movement
        for i in range(math.ceil(abs(self.hsp))):
            collision_check_rect = self.rect.move(sign(self.hsp),0)
            if self.x == player_offset_x:
                break
            elif collision_check_rect.collidelistall(self.solid_rect_list)\
            or collision_check_rect.collidelistall(self.slope_rect_list):
                self.hsp = 0
                break
            self.x += sign(self.hsp)
            self.rect.x = self.x
            self.rect.y = self.y
        #Shoot bullets
        if self.difference_vector.length() <= self.range:
            self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.difference_vector.length() <= self.range:
            self.shoot_bullet_timer = 0
            self.bullet_dir_1[0] = self.shooting_dir 
            self.bullet_dir_2[0] = self.shooting_dir 
            random_distance = random.randint(-25,20)
            enemy_bullets.add_wavy_bullet(self.rect.centerx+(random_distance*self.facing),self.rect.centery,self.bullet_dir_1[:],self.bullet_x_stretch,self.bullet_y_stretch,self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
            enemy_bullets.add_wavy_bullet(self.rect.centerx+(random_distance*self.facing),self.rect.centery,self.bullet_dir_2[:],self.bullet_x_stretch,self.bullet_y_stretch,self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
    def reset(self):
        super().reset()
        #General Attributes
        self.image = pygame.image.load("Images/Enemies/villiform_man_1.png").convert_alpha()
        self.rect = pygame.image.load("Images/Enemies/villiform_man_hitbox.png").get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.dir = 1
        self.shooting_dir = 0 #Left or right from player, which way to shoot, determines player offset
        self.health = 20
        #Animations
        self.draw_offset = 23
        self.facing = 1
        self.normal_animation = [[pygame.image.load("Images/Enemies/villiform_man_1.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/villiform_man_2.png").convert_alpha(),5],[pygame.image.load("Images/Enemies/villiform_man_3.png").convert_alpha(),5]]
        self.animation = self.normal_animation
        #Shooting
        #[x,y,rect,[dir_x,dir_y],speed,decay]
        self.difference_vector = pygame.math.Vector2(0,0)
        self.target_vector = pygame.math.Vector2(0,0)
        self.bullet_animation = [[pygame.image.load("Images/Bullets/enemy_wavy_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_wavy_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Bullets/enemy_wavy_bullet_3.png").convert_alpha(),5]]
        self.shoot_bullet_timer = 0
        self.shoot_bullet_max = 70
        self.bullet_dir_1 = [-1,-1]
        self.bullet_dir_2 = [-1,1]
        self.bullet_x_stretch = 1/80
        self.bullet_y_stretch = 150
        self.bullet_speed = 3
        self.bullet_decay = 200 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rect and positioning
        self.bullet_rect_height = 12
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Bullets/enemy_wavy_bullet_1.png"))
        #Normal State
        self.normal_speed = 2
        self.normal_distance_from_player = 250 #Moves away from player to certian range
        self.range = 400
