from Enemies import Enemy
from General_Functions import *
from Bullets import *

"""
Player.
Has different states, can do slope mask collision.
"""
class Player(): 
    def __init__(self,x,y): 
        self.start_x = x
        self.start_y = y
        self.reset()
    def update(self,game_state_manager,input_dict,tilemap,instances,enemy_bullets,death_screen): #Only arguments should be self, game_state_manager, input_dict and collisions
        #Falling off level
        if self.y >= tilemap.level_height:
            self.state = self.states["Dead"]
            self.next_state = self.states["Dead"]
        if self.x < 0:
            self.x = 0
        if self.x > tilemap.level_width - self.rect.width:
            self.x = tilemap.level_width - self.rect.width
        #Screen Shake
        if self.shooting_screen_shake_timer > 0:
            self.shooting_screen_shake_timer -= 1
        if self.sheild_screen_shake_timer > 0:
            self.sheild_screen_shake_timer -= 1
        if self.hurt_screen_shake_timer > 0:
            self.hurt_screen_shake_timer -= 1
        #Tiles
        self.solid_rect_list = tilemap.tile_rect_dict["solid_rect_list"]
        self.hazard_rect_list = tilemap.tile_rect_dict["hazard_rect_list"]
        self.jump_through_platform_rect_list = tilemap.tile_rect_dict["jump_through_platform_rect_list"]
        self.slope_rect_list = tilemap.tile_rect_dict["slope_rect_list"]
        self.enemy_solid_rect_list = tilemap.tile_rect_dict["enemy_solid_rect_list"]
        #Slopes
        self.slope_mask_list = tilemap.slope_mask_list
        #Instances
        self.enemy_list = instances.instance_dict["enemy_list"]
        #Bullets
        self.enemy_bullet_list = enemy_bullets.bullet_list
        self.enemy_lobber_list = enemy_bullets.lobber_list
        self.enemy_wavy_bullet_list = enemy_bullets.wavy_bullet_list
        #Sheild
        if self.sheild_charged:
            self.current_pointer_animation = self.pointer_animation
            if self.sheild_key:
                self.sheild_on = True
                self.sheild_timer += 2
                if self.sheild_timer < (1/4 * self.sheild_max):
                    self.sheild_image = self.sheild_normal_image
                elif self.sheild_timer < (1/2 * self.sheild_max):
                    self.sheild_image = self.sheild__high_image
                elif self.sheild_timer < (3/4 * self.sheild_max):
                    self.sheild_image = self.sheild_med_image
                else:
                    self.sheild_image = self.sheild_low_image
            else:
                self.sheild_on = False
                if self.sheild_timer > 0:
                    self.sheild_timer -= 1
        else:
            self.current_pointer_animation = self.pointer_sheild_off_animation
            self.sheild_on = False
            self.sheild_timer += 2
        if self.sheild_timer >= self.sheild_max:
            self.sheild_charged = not self.sheild_charged
            self.sheild_timer = 0
        #Get Inputs
        self.shooting_key = input_dict["shooting_key"]
        self.sheild_key = input_dict["sheild_key"]
        self.controller = input_dict["controller"]
        self.aiming_input = input_dict["aiming_input"]
        self.left_key = input_dict["left_key"]
        self.right_key = input_dict["right_key"]
        self.down_key = input_dict["down_key"]
        self.jump_key_down = input_dict["jump_key_down"]
        self.jump_key_up = input_dict["jump_key_up"]
        self.dash_key = input_dict["dash_key"]
        self.pause_key = input_dict["pause_key"]
        #Pause
        if self.pause_key:
            game_state_manager.state = game_state_manager.states["Pause"]
            return
        #Switch States
        if self.state != self.next_state:
            self.state = self.next_state
            #What you need to do at the start of the state
            if self.state[0]:
                self.state[0]()
        if self.state == self.states["Dead"]:
            self.state[1](game_state_manager,death_screen)
        else:
            self.state[1](game_state_manager,enemy_bullets)
    #Seperate from update, needs camera as relative to player position, 
    #and player_bullets to add bullets. Updates aiming and shooting
    def update_shooting(self,camera,player_bullets):
        if self.sheild_on:
            self.reticle_rect = self.sheild_rect
            self.shoot_bullet_timer = 0
        else:
            self.reticle_rect = self.shooting_reticle_rect
        #Working out where you are aiming based on input
        player_relative_screen_vector = pygame.math.Vector2(self.rect.centerx-camera.x,self.rect.centery-camera.y)
        if self.controller == False:
            aiming_input_vector = pygame.math.Vector2(self.aiming_input)
            temp_aiming_vector = aiming_input_vector - player_relative_screen_vector
            if temp_aiming_vector.length() != 0:
                self.aiming_vector = temp_aiming_vector
        else:
            if not (self.aiming_input[0] == 0 and self.aiming_input[1] == 0):  
                self.aiming_vector = pygame.math.Vector2(self.aiming_input[0],self.aiming_input[1])
        #Normalising aiming vector, working out reticle position and aiming angle 
        if self.aiming_vector.length() != 0:
            self.aiming_vector = self.aiming_vector.normalize() 
            self.reticle_rect.center = (self.rect.centerx+(self.aiming_vector.x*self.reticle_distance_from_player),self.rect.centery+(self.aiming_vector.y*self.reticle_distance_from_player))
            self.aiming_angle = 180 + math.degrees(math.atan2(self.aiming_vector.x,self.aiming_vector.y))
        #Cannot normalise reticle length 0
        else:
            self.reticle_rect.center = (self.rect.centerx+(self.aiming_vector.x*self.reticle_distance_from_player),self.rect.centery+(self.aiming_vector.y*self.reticle_distance_from_player))     
        #Updating shooting
        self.shoot_bullet_timer += 1
        if self.shoot_bullet_timer >= self.shoot_bullet_max and self.shooting_key and not self.sheild_key and not self.rect.collidelistall(self.enemy_solid_rect_list):
            self.shoot_bullet_timer = 0
            if self.charge_bullet_timer >= self.charge_bullet_max:
                player_bullets.add_bullet(self.reticle_rect.centerx,self.reticle_rect.centery,[self.aiming_vector.x,self.aiming_vector.y],self.charge_bullet_rect_width,self.charge_bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.charge_bullet_animation,self.charge_bullet_damage)
                self.charge_bullet_timer = 0
            else:
                player_bullets.add_bullet(self.reticle_rect.centerx,self.reticle_rect.centery,[self.aiming_vector.x,self.aiming_vector.y],self.bullet_rect_width,self.bullet_rect_height,self.bullet_mask,self.bullet_speed,self.bullet_decay,self.bullet_animation)
                self.charge_bullet_timer = 0
            self.shooting_screen_shake_timer = self.shooting_screen_shake_max
        elif not (self.shooting_key and not self.sheild_key):
            self.charge_bullet_timer += 1
    def draw(self,screen,camera):
        self.current_frame = animation(self.animation,self.current_frame)
        self.image = self.animation[self.current_frame[0]][0]
        draw_rect = self.image.get_rect()
        draw_rect.x = self.rect.x - 22 - camera.x
        draw_rect.y = self.rect.y - 37 - camera.y
        if self.dir_facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            draw_rect.x -= 26 #Compensate for trunk which isn't part of hitbox
        if self.invincibility_timer < self.invincibility_max:
            self.invincibility_flash_timer += 1
            if self.invincibility_flash_timer >= self.invincibility_flash_max:
                self.invincibility_flash = not self.invincibility_flash 
                self.invincibility_flash_timer = 0
            if self.invincibility_flash:
                self.image = pygame.Surface((0,0),pygame.SRCALPHA)
            else:
                image_mask = pygame.mask.from_surface(self.image)
                self.image = image_mask.to_surface(unsetcolor = None)
        else:
            self.invincibility_flash_timer = 0 
        screen.blit(self.image,(draw_rect.x,draw_rect.y))
        """
        #Draw player's collision rects
        draw_rect_rect = self.rect.move(-camera.x,-camera.y)
        pygame.draw.rect(screen,(0,255,0),draw_rect_rect)
        hurtbox_draw_rect = self.hurtbox.move(-camera.x,-camera.y)
        pygame.draw.rect(screen,(255,255,0),hurtbox_draw_rect)
        """
        #Jump Effect
        for effect in self.jump_effect_list[:]:
            #Effect is [x,y,current_frame]
            effect[2] = animation(self.jump_effect_animation,effect[2],False)
            if not effect[2]:
                self.jump_effect_list.remove(effect)
            else:
                screen.blit(self.jump_effect_animation[effect[2][0]][0],(effect[0]-camera.x,effect[1]-camera.y))
        #Dash Effect
        for effect in self.dash_effect_list[:]:
            #Effect is [x,y,current_frame]
            effect[2] = animation(self.dash_effect_animation,effect[2],False)
            if not effect[2]:
                self.dash_effect_list.remove(effect)
            else:
                if effect[3] == -1:
                    screen.blit(pygame.transform.flip(self.dash_effect_animation[effect[2][0]][0],True,False),(effect[0]-camera.x,effect[1]-camera.y))
                else:
                      screen.blit(self.dash_effect_animation[effect[2][0]][0],(effect[0]-camera.x,effect[1]-camera.y))
    #Needs to be drawn above everything else
    def draw_aiming_reticle(self,screen,camera):
        if self.sheild_on:
            reticle_image_transformed = self.sheild_image
        elif self.charge_bullet_timer >= self.charge_bullet_max:
            if self.sheild_charged:
                reticle_image_transformed = pygame.transform.rotate(self.charge_reticle_image,self.aiming_angle)
            else:
                reticle_image_transformed = pygame.transform.rotate(self.charge_reticle_sheild_off_image,self.aiming_angle)
        else:
            if self.sheild_charged:
                reticle_image_transformed = pygame.transform.rotate(self.reticle_image,self.aiming_angle)
            else:
                reticle_image_transformed = pygame.transform.rotate(self.reticle_sheild_off_image,self.aiming_angle)
        screen.blit(reticle_image_transformed,(self.reticle_rect.x-camera.x,self.reticle_rect.y-camera.y))
        if self.health >= 4 and self.health_face_animation != self.high_health_face_animation:
            self.health_face_animation = self.high_health_face_animation
            self.current_frame = [0,0]
        elif self.health == 3 and self.health_face_animation != self.good_health_face_animation:
            self.health_face_animation = self.good_health_face_animation
            self.current_frame = [0,0]
        elif self.health == 2 and self.health_face_animation != self.medium_health_face_animation:
            self.health_face_animation = self.medium_health_face_animation
            self.current_frame = [0,0]
        elif self.health <= 1 and self.health_face_animation != self.low_health_face_animation:
            self.health_face_animation = self.low_health_face_animation
            self.current_frame = [0,0]
        self.health_face_current_frame = animation(self.health_face_animation,self.health_face_current_frame)
        screen.blit(self.health_face_animation[self.health_face_current_frame[0]][0],(0,0))
        self.trunk_heart_current_frame = animation(self.trunk_heart_animation,self.trunk_heart_current_frame)
        x = 140
        for i in range(self.health):
            screen.blit(self.trunk_heart_animation[self.trunk_heart_current_frame[0]][0],(x,5))
            x += 110
        #Draw pointer
        if self.aiming_input and self.controller == False:
            self.pointer_rect.centerx = self.aiming_input[0]
            self.pointer_rect.centery = self.aiming_input[1]
            self.pointer_current_frame = animation(self.current_pointer_animation,self.pointer_current_frame)
            screen.blit(self.current_pointer_animation[self.pointer_current_frame[0]][0],(self.pointer_rect.x,self.pointer_rect.y))
    def normal_start(self):
        if self.animation != self.dash_animation: #Should stay dashing
            self.animation,self.current_frame = switch_animation(self.animation,self.walk_animation,self.current_frame,switch_always=True)
    def normal(self,game_state_manager,enemy_bullets):
        #Initial collision checks for moving objects
        if self.invincibility_timer >= self.invincibility_max:
            #Enemy Collision
            for enemy in self.enemy_list:
                if self.hurtbox.colliderect(enemy.rect):
                    self.health -= 1
                    self.invincibility_timer = 0
                    self.hurt_screen_shake_timer = self.hurt_screen_shake_max
                    break
            self.bullet_collision_check(enemy_bullets)
        else:
            self.invincibility_timer += 1
        if self.health <= 0:
            self.state = self.states["Dead"]
            self.next_state = self.states["Dead"]
            return
        #Direction
        move = self.right_key - self.left_key
        if move != 0:
            self.dir_facing = move
        #Dash
        if self.grounded:
            self.dash_count = 0
            if self.animation == self.dash_animation: #Switch from dash animation
                self.animation,self.current_frame = switch_animation(self.animation,self.walk_animation,self.current_frame,[3,0])
        if self.dash_key and self.dash_count == 0:
            self.hsp = self.dash_hdistance * self.dir_facing
            self.vsp = -self.dash_vdistance 
            self.animation,self.current_frame = switch_animation(self.animation,self.dash_animation,self.current_frame,switch_always=False)
            self.dash_effect_list.append([self.x,self.y,[0,0],self.dir_facing])
            self.dash_count = 1
        #Jump Buffer
        if self.jump_key_down:
            self.jump_buffer_timer = 0
        if self.jump_buffer_timer < self.jump_buffer_max:
            self.jump_buffer_timer += 1
        #Coyote Jump
        if self.grounded == True:
            self.coyote_jump_timer = 0
        #Jump 
        if self.coyote_jump_timer < self.coyote_jump_max:
            self.coyote_jump_timer += 1
        if self.jump_buffer_timer < self.jump_buffer_max and self.coyote_jump_timer < self.coyote_jump_max:
            self.next_state = self.states["Jumping"]
        if not self.dash_key:
            #Setting Horizontal Speed
            #Changes accleration if in ground or air
            if self.grounded:
                acceleration = self.normal_ground_acceleration
                decceleration = self.normal_ground_decceleration
                friction = self.normal_ground_friction
            else:
                acceleration = self.normal_air_acceleration
                decceleration = self.normal_air_decceleration
                friction = self.normal_air_friction
            #Slow down if no keys are pressed
            if move == 0:
                if (abs(self.hsp) - friction) < 0:
                    self.hsp = 0
                else:
                    self.hsp -= (sign(self.hsp) * friction)
                if self.animation != self.dash_animation: #Should stay dashing
                    self.animation,self.current_frame = switch_animation(self.animation,self.idle_animation,self.current_frame)
            else:
                if move == sign(self.hsp):
                    normal_speed = abs(self.hsp)
                    if normal_speed <= self.normal_speed_max: #Allows dash to be faster
                        normal_speed += acceleration
                        normal_speed = min(normal_speed,self.normal_speed_max)
                    else:
                        normal_speed += acceleration
                        normal_speed = min(normal_speed,self.dash_hdistance)
                #Accelerate faster from stop or when turning
                else:
                    normal_speed = -abs(self.hsp)
                    normal_speed += decceleration
                self.hsp = move * normal_speed
                if self.animation != self.dash_animation: #Should stay dashing
                    self.animation,self.current_frame = switch_animation(self.animation,self.walk_animation,self.current_frame,[3,0])
            #Setting Vertical Speed
            self.vsp += self.grv
            self.vsp = min(self.max_grv,self.vsp)
        #Sub Pixel Stuff
        self.sub_pixel_hsp += self.hsp
        self.sub_pixel_vsp += self.vsp
        trunc_hsp = math.trunc(self.sub_pixel_hsp)
        trunc_vsp = math.trunc(self.sub_pixel_vsp)
        self.sub_pixel_hsp -= trunc_hsp
        self.sub_pixel_vsp -= trunc_vsp
        #Vertical Collision
        for i in range(abs(trunc_vsp)):
            #Sheild Collision
            self.sheild_collision_check(enemy_bullets)
            #Slope Collision
            slope_collision_check_rect = self.rect.move(0,sign(self.vsp))
            all_slope_collision_checks = slope_collision_check_rect.collidelistall(self.slope_rect_list)
            all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
            slope_collision = False
            #Checks all slope masks that the player has collided withs rects. There indexes are the same as the lists are in the same order
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                #This means that if the player moves down 1 (+1), the slopes position is closer to the player (-1)
                #That's why it is -sign(hsp) and +1 instead of -1 etc
                slope_offset_x = mask_data[1] - self.x
                slope_offset_y = mask_data[2] - self.y
                if self.mask.overlap(mask_data[0],(slope_offset_x,slope_offset_y-sign(self.vsp))):
                    if sign(self.vsp) == -1:
                        slope_collision = True
                        self.grounded = False
                        break
                    else:
                        slope_collision = True
                        self.vsp = 0
                        self.grounded = True
                        break
            if slope_collision == True:
                break
            #Tile Collision
            tile_collision_check_rect = self.rect.move(0,sign(self.vsp))
            #Solid Collision
            if tile_collision_check_rect.collidelistall(self.solid_rect_list):
                if sign(self.vsp) == -1:
                    break
                else:
                    self.vsp = 0
                    self.grounded = True
                    break
            #Hazard Collision
            elif tile_collision_check_rect.collidelistall(self.hazard_rect_list):
                self.state = self.states["Dead"]
                self.next_state = self.states["Dead"]
                return
            #Jump Through Platform Collision
            if tile_collision_check_rect.collidelistall(self.jump_through_platform_rect_list)\
            and not self.rect.collidelistall(self.jump_through_platform_rect_list) and sign(self.vsp) != -1 and not self.down_key:
                self.vsp = 0
                self.grounded = True
                break
            #Move if not collided
            self.y += sign(self.vsp)
            self.rect.x = self.x
            self.rect.y = self.y
            self.hurtbox.center = self.rect.center
            self.grounded = False
        #Horizontal Collision
        for i in range(abs(trunc_hsp)):
            #Sheild Collision
            self.sheild_collision_check(enemy_bullets)
            #Slope Collision
            #Mask Data has [mask,x,y]
            slope_collision_check_rect = self.rect.move(sign(self.hsp),0)
            slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
            slope_collision_check_rect_down = self.rect.move(sign(self.hsp),2)
            slope_rect_down_collision_check = slope_collision_check_rect_down.collidelistall(self.slope_rect_list)
            all_slope_collision_checks = slope_rect_collision_check + slope_rect_down_collision_check
            all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
            already_moved_slope = False
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                #This means that if the player moves down 1 (+1), the slopes position is closer to the player, making it relatively higher (-1)
                #That's why it is -sign(hsp) and +1 instead of -1 etc
                slope_offset_x = mask_data[1] - self.x
                slope_offset_y = mask_data[2] - self.y
                #Moving Up Slopes
                if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y)):
                    #Check if you don't collide with something else
                    can_move_up_slope = True
                    #Collided with Solid
                    solid_collision_check_rect_up = self.rect.move(sign(self.hsp),-1) 
                    solid_rect_up_collision_check = solid_collision_check_rect_up.collidelistall(self.solid_rect_list)
                    if solid_rect_up_collision_check:
                        can_move_up_slope = False
                        self.hsp = 0
                    else:
                        #Collide with Slope so you can't move up
                        slope_collision_check_rect_up = self.rect.move(sign(self.hsp),-1)
                        slope_rect_up_collision_check = slope_collision_check_rect_up.collidelistall(self.slope_rect_list)
                        all_slope_collision_checks = slope_rect_up_collision_check
                        all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
                        for index in all_slope_collision_checks:
                            mask_data = self.slope_mask_list[index]
                            slope_offset_x = mask_data[1] - self.x
                            slope_offset_y = mask_data[2] - self.y
                            if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y+1)):
                                can_move_up_slope = False
                                self.hsp = 0
                                break
                    if can_move_up_slope == True:
                        self.x += sign(self.hsp)
                        self.y -= 1
                        self.rect.x = self.x
                        self.rect.y = self.y
                        self.hurtbox.center = self.rect.center
                        already_moved_slope = True
                        self.grounded = True
                        break
                #Moving Down Slopes
                if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y-2)):
                    can_move_down_slope = True
                    #Collision with solid that will be checked later
                    solid_collision_check_rect = self.rect.move(sign(self.hsp),0)
                    solid_rect_collision_check = solid_collision_check_rect.collidelistall(self.solid_rect_list)
                    if solid_rect_collision_check:
                        can_move_down_slope = False
                    else:
                        slope_collision_check_rect = self.rect.move(sign(self.hsp),0)
                        slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
                        slope_collision_check_rect_down = self.rect.move(sign(self.hsp),1)
                        slope_rect_down_collision_check = slope_collision_check_rect_down.collidelistall(self.slope_rect_list)
                        all_slope_collision_checks = slope_rect_collision_check + slope_rect_down_collision_check
                        all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
                        for index in all_slope_collision_checks:
                            mask_data = self.slope_mask_list[index]
                            slope_offset_x = mask_data[1] - self.x
                            slope_offset_y = mask_data[2] - self.y
                            #May be that you can move up the slope next frame
                            if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y)):
                                can_move_down_slope = False
                                break
                            #On top of the slope and should still move in this frame
                            elif self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y-1)):
                                can_move_down_slope = False
                                break
                    if can_move_down_slope == True:
                        self.x += sign(self.hsp)
                        self.y += 1
                        self.rect.x = self.x
                        self.rect.y = self.y
                        self.hurtbox.center = self.rect.center
                        already_moved_slope = True
                        self.grounded = True
                        break
            #Going down slope to solid
            solid_collision_check_rect_down = self.rect.move(sign(self.hsp),2)
            if solid_collision_check_rect_down.collidelistall(self.solid_rect_list):
                can_move_down_slope = True
                #Collision with solid that will be checked later
                solid_collision_check_rect = self.rect.move(sign(self.hsp),0)            
                solid_rect_collision_check = solid_collision_check_rect.collidelistall(self.solid_rect_list)
                solid_collision_check_rect_down = self.rect.move(sign(self.hsp),1)
                solid_rect_down_collision_check = solid_collision_check_rect_down.collidelistall(self.solid_rect_list)
                all_solid_collision_checks = solid_rect_collision_check + solid_rect_down_collision_check
                if all_solid_collision_checks:
                    can_move_down_slope = False
                else:
                    slope_collision_check_rect = self.rect.move(sign(self.hsp),0)
                    slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
                    slope_collision_check_rect_down = self.rect.move(sign(self.hsp),1)
                    slope_rect_down_collision_check = slope_collision_check_rect_down.collidelistall(self.slope_rect_list)
                    all_slope_collision_checks = slope_rect_collision_check + slope_rect_down_collision_check
                    all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
                    for index in all_slope_collision_checks:
                        mask = self.slope_mask_list[index]
                        slope_offset_x = mask_data[1] - self.x
                        slope_offset_y = mask_data[2] - self.y
                        if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y)):
                            can_move_down_slope = False
                            slope_collision = True
                            break
                        #You are on top of the slope and should still move in this frame
                        elif self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y-1)):
                            can_move_down_slope = False
                            break
                    if can_move_down_slope == True:
                        self.x += sign(self.hsp)
                        self.y += 1
                        self.rect.x = self.x
                        self.rect.y = self.y
                        self.hurtbox.center = self.rect.center
                        already_moved_slope = True
                        self.grounded = True
            #Tile Collision
            tile_collision_check_rect = self.rect.move(sign(self.hsp),0)
            #Solid Collision
            if tile_collision_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                break
            #Hazard Collision
            elif tile_collision_check_rect.collidelistall(self.hazard_rect_list):
                self.state = self.states["Dead"]
                self.next_state = self.states["Dead"]
                return
            #If you haven't already moved on a slope
            if already_moved_slope == False:
                self.x += sign(self.hsp)
                self.rect.x = self.x
                self.rect.y = self.y
                self.hurtbox.center = self.rect.center
        #Sheild
        #ALSO BEFORE MOVING
        self.sheild_collision_check(enemy_bullets)
    def jumping_start(self):
        self.vsp = self.jump_height
        self.jump_buffer_timer = self.jump_buffer_max
        self.coyote_jump_timer = self.coyote_jump_max
        self.animation,self.current_frame = switch_animation(self.animation,self.jump_animation,self.current_frame,switch_always=True)
        self.grounded = False
        self.jump_effect_list.append([self.x,self.y,[0,0]])
    def jumping(self,game_state_manager,enemy_bullets):
        #Initial collision checks for moving objects
        if self.invincibility_timer >= self.invincibility_max:
            #Enemy Collision
            for enemy in self.enemy_list:
                if self.hurtbox.colliderect(enemy.rect):
                    self.health -= 1
                    self.invincibility_timer = 0
                    self.hurt_screen_shake_timer = self.hurt_screen_shake_max
                    break
            self.bullet_collision_check(enemy_bullets)
        else:
            self.invincibility_timer += 1
        if self.health <= 0:
            self.state = self.states["Dead"]
            self.next_state = self.states["Dead"]
            return
        #Direction
        move = self.right_key - self.left_key
        if move != 0:
            self.dir_facing = move
        #Dash
        if self.grounded:
            self.dash_count = 0
            if self.animation == self.dash_animation: #Switch from dash animation
                self.animation,self.current_frame = switch_animation(self.animation,self.walk_animation,self.current_frame,[3,0])
        if self.dash_key and self.dash_count == 0:
            self.hsp = self.dash_hdistance * self.dir_facing
            self.vsp = -self.dash_vdistance
            self.state = self.states["Normal"]
            self.next_state = self.states["Normal"]
            self.animation,self.current_frame = switch_animation(self.animation,self.dash_animation,self.current_frame,switch_always=False)
            self.dash_effect_list.append([self.x,self.y,[0,0],self.dir_facing])
            self.dash_count = 1
            return
        #Jump Buffer
        if self.jump_key_down:
            self.jump_buffer_timer = 0
        if self.jump_buffer_timer < self.jump_buffer_max:
            self.jump_buffer_timer += 1
        #Variable Jump Height
        if self.jump_key_up and sign(self.vsp) == -1:
            self.vsp += -self.vsp/4
            self.jump_buffer_timer = self.jump_buffer_max
            self.coyote_jump_timer = self.coyote_jump_max
        if not self.dash_key:
            #Setting Speed
            acceleration = self.normal_air_acceleration
            decceleration = self.normal_air_decceleration
            friction = self.normal_air_friction
            if move == 0:
                if (abs(self.hsp) - friction) < 0:
                    self.hsp = 0
                else:
                    self.hsp -= (sign(self.hsp) * friction)
            else:
                if move == sign(self.hsp):
                    normal_speed = abs(self.hsp)
                    normal_speed = abs(self.hsp)
                    if normal_speed <= self.normal_speed_max: #Allows dash to be faster
                        normal_speed += acceleration
                        normal_speed = min(normal_speed,self.normal_speed_max)
                    else:
                        normal_speed += acceleration
                        normal_speed = min(normal_speed,self.dash_hdistance)
                #Accelerate faster from stop or when turning
                else:
                    normal_speed = -abs(self.hsp)
                    normal_speed += decceleration
                self.hsp = move * normal_speed
            #Hang Time
            if abs(self.vsp) <= self.hang_time_check and not self.dash_key:
                self.vsp += self.grv * self.hang_time_multiplier
            else:
                self.vsp += self.grv
            self.vsp = min(self.max_grv,self.vsp)
        #Sub Pixel Stuff
        self.sub_pixel_hsp += self.hsp
        self.sub_pixel_vsp += self.vsp
        trunc_hsp = math.trunc(self.sub_pixel_hsp)
        trunc_vsp = math.trunc(self.sub_pixel_vsp)
        self.sub_pixel_hsp -= trunc_hsp
        self.sub_pixel_vsp -= trunc_vsp
        #Animations
        if sign(self.sub_pixel_vsp) == -1 or sign(self.sub_pixel_vsp) == 0:
            self.animation,self.current_frame = switch_animation(self.animation,self.jump_animation,self.current_frame)
        else:
            self.animation,self.current_frame = switch_animation(self.animation,self.fall_animation,self.current_frame)
        #Vertical Collision
        for i in range(abs(trunc_vsp)):
            #Sheild Collision
            self.sheild_collision_check(enemy_bullets)
            #Slope Collision
            slope_collision = False
            slope_collision_check_rect = self.rect.move(0,sign(self.vsp))
            slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
            all_slope_collision_checks = slope_rect_collision_check
            all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                #This means that if the player moves down 1 (+1), the slopes position is closer to the player (-1)
                #That's why it is -sign(hsp) and +1 instead of -1 etc
                slope_offset_x = mask_data[1] - self.x
                slope_offset_y = mask_data[2] - self.y
                if self.mask.overlap(mask_data[0],(slope_offset_x,slope_offset_y-sign(self.vsp))):
                    if sign(self.vsp) == -1:
                        slope_collision = True
                        self.vsp = 0
                        break
                    else:
                        slope_collision = True
                        self.grounded = True
                        self.vsp = 0
                        break
            if self.grounded == True:
                self.next_state = self.states["Normal"]
            #So you stick to the roof
            if slope_collision == True:
                break
            #Tile Collision
            tile_collision_check_rect = self.rect.move(0,sign(self.vsp))
            #Solid Collision
            if tile_collision_check_rect.collidelistall(self.solid_rect_list):
                if sign(self.vsp) == -1:
                    break
                else:
                    self.vsp = 0
                    self.grounded = True
                    self.next_state = self.states["Normal"]
                    break
            #Hazard Collision
            elif tile_collision_check_rect.collidelistall(self.hazard_rect_list):
                self.state = self.states["Dead"]
                self.next_state = self.states["Dead"]
                return
            #Jump Through Platform Collision
            if tile_collision_check_rect.collidelistall(self.jump_through_platform_rect_list)\
            and not self.rect.collidelistall(self.jump_through_platform_rect_list) and sign(self.vsp) != -1 and not self.down_key:
                self.vsp = 0
                self.grounded = True
                self.next_state = self.states["Normal"]
                break
            self.y += sign(self.vsp)
            self.rect.x = self.x
            self.rect.y = self.y
            self.hurtbox.center = self.rect.center
        #Horizontal Collision
        for i in range(abs(trunc_hsp)):
            #Sheild Collision
            self.sheild_collision_check(enemy_bullets)
            #Slope Collision
            #Mask Data has [mask,x,y]
            slope_collision = False
            slope_collision_check_rect = self.rect.move(sign(self.hsp),0)
            slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
            slope_collision_check_rect_down = self.rect.move(sign(self.hsp),2)
            slope_rect_down_collision_check = slope_collision_check_rect_down.collidelistall(self.slope_rect_list)
            all_slope_collision_checks = slope_rect_collision_check + slope_rect_down_collision_check
            all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
            for index in all_slope_collision_checks:
                mask_data = self.slope_mask_list[index]
                #Offset is imagining that self.mask is (0,0), so where is the slope mask
                #This means that if the player moves down 1 (+1), the slopes position is closer to the player, making it relatively higher (-1)
                #That's why it is -sign(hsp) and +1 instead of -1 etc
                slope_offset_x = mask_data[1] - self.x
                slope_offset_y = mask_data[2] - self.y
                #Moving Up Slopes
                if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y)):
                    #Check if you don't collide with something else
                    can_move_up_slope = True
                    #Collided with Solid
                    solid_collision_check_rect_up = self.rect.move(sign(self.hsp),-1) 
                    solid_rect_up_collision_check = solid_collision_check_rect_up.collidelistall(self.solid_rect_list)
                    if solid_rect_up_collision_check:
                        can_move_up_slope = False
                        self.hsp = 0
                    else:
                        #Collide with Slope so you can't move up
                        slope_collision_check_rect_up = self.rect.move(sign(self.hsp),-1)
                        slope_rect_up_collision_check = slope_collision_check_rect_up.collidelistall(self.slope_rect_list)
                        all_slope_collision_checks = slope_rect_up_collision_check
                        all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
                        for index in all_slope_collision_checks:
                            mask_data = self.slope_mask_list[index]
                            slope_offset_x = mask_data[1] - self.x
                            slope_offset_y = mask_data[2] - self.y
                            if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y+1)):
                                can_move_up_slope = False
                                self.hsp = 0
                                break
                    if can_move_up_slope == True:
                        slope_collision = True
                        self.grounded = True
                        self.vsp = 0      
                #Moving Down Slopes
                elif self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y-2)):
                    #Checks if you are not colliding with another slope
                    can_move_down_slope = True
                    #Collision with solid that will be checked later
                    solid_collision_check_rect = self.rect.move(sign(self.hsp),0)
                    solid_rect_collision_check = solid_collision_check_rect.collidelistall(self.solid_rect_list)
                    if solid_rect_collision_check:
                        can_move_down_slope = False
                    else:
                        slope_collision_check_rect = self.rect.move(sign(self.hsp),0)
                        slope_rect_collision_check = slope_collision_check_rect.collidelistall(self.slope_rect_list)
                        slope_collision_check_rect_down = self.rect.move(sign(self.hsp),1)
                        slope_rect_down_collision_check = slope_collision_check_rect_down.collidelistall(self.slope_rect_list)
                        all_slope_collision_checks = slope_rect_collision_check + slope_rect_down_collision_check
                        all_slope_collision_checks = delete_duplicates_from_list(all_slope_collision_checks)
                        for index in all_slope_collision_checks:
                            mask_data = self.slope_mask_list[index]
                            slope_offset_x = mask_data[1] - self.x
                            slope_offset_y = mask_data[2] - self.y
                            if self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y)):
                                can_move_down_slope = False
                                break
                            elif self.mask.overlap(mask_data[0],(slope_offset_x-sign(self.hsp),slope_offset_y-1)):
                                can_move_down_slope = False
                                break
                    if can_move_down_slope == True:
                        slope_collision = True
                        self.grounded = True
                        self.vsp = 0   
            #Can't be if self.grounded == True because you still need to move horizontally if you hit the ground on vertical collision
            if slope_collision == True:
                self.next_state = self.states["Normal"]
                break
            #Tile Collision
            tile_collision_check_rect = self.rect.move(sign(self.hsp),0)
            #Solid Collision
            if tile_collision_check_rect.collidelistall(self.solid_rect_list):
                self.hsp = 0
                break
            #Hazard Collision
            elif tile_collision_check_rect.collidelistall(self.hazard_rect_list):
                self.state = self.states["Dead"]
                self.next_state = self.states["Dead"]
                return
            self.x += sign(self.hsp)
            self.rect.x = self.x
            self.rect.y = self.y
            self.hurtbox.center = self.rect.center
        #Sheild
        #ALSO BEFORE MOVING
        self.sheild_collision_check(enemy_bullets)
    def swimming(self,game_state_manager,enemy_bullets):
        pass
    def dead(self,game_state_manager,death_screen):
        game_state_manager.state = game_state_manager.states["Dead"]
        if self.controller:
            death_screen.controller_trigger_held = self.shooting_key
    #General Functions
    def bullet_collision_check(self,enemy_bullets):
        #Bullet Collision
        bullet_index = 0
        for bullet in self.enemy_bullet_list:
            if self.hurtbox.colliderect(bullet["rect"]):
                self.health -= enemy_bullets.bullet_list[bullet_index]["damage"]
                enemy_bullets.bullet_list[bullet_index]["decay"] = 0
                enemy_bullets.bullet_list[bullet_index]["rect"] = pygame.Rect(0,0,0,0)
                self.invincibility_timer = 0
                self.hurt_screen_shake_timer = self.hurt_screen_shake_max
                break
            bullet_index += 1
        bullet_index = 0
        for bullet in self.enemy_lobber_list:
            if self.hurtbox.colliderect(bullet["rect"]):
                self.health -= enemy_bullets.lobber_list[bullet_index]["damage"]
                enemy_bullets.lobber_list[bullet_index]["decay"] = 0
                enemy_bullets.lobber_list[bullet_index]["rect"] = pygame.Rect(0,0,0,0)
                self.invincibility_timer = 0
                self.hurt_screen_shake_timer = self.hurt_screen_shake_max
                break
            bullet_index += 1
        bullet_index = 0
        for bullet in self.enemy_wavy_bullet_list:
            if self.hurtbox.colliderect(bullet["rect"]):
                self.health -= enemy_bullets.wavy_bullet_list[bullet_index]["damage"]
                enemy_bullets.wavy_bullet_list[bullet_index]["decay"] = 0
                enemy_bullets.wavy_bullet_list[bullet_index]["rect"] = pygame.Rect(0,0,0,0)
                self.invincibility_timer = 0
                self.hurt_screen_shake_timer = self.hurt_screen_shake_max
                break
            bullet_index += 1
    def sheild_collision_check(self,enemy_bullets):
        if self.sheild_on:
            bullet_index = 0
            for bullet in self.enemy_bullet_list:
                if self.reticle_rect.colliderect(bullet["rect"]):
                    enemy_bullets.bullet_list[bullet_index]["decay"] = 0
                    self.sheild_screen_shake_timer = self.sheild_screen_shake_max
                    break
                bullet_index += 1
            bullet_index = 0
            for bullet in self.enemy_lobber_list:
                if self.reticle_rect.colliderect(bullet["rect"]):
                    enemy_bullets.lobber_list[bullet_index]["decay"] = 0
                    self.sheild_screen_shake_timer = self.sheild_screen_shake_max
                    break
                bullet_index += 1
            bullet_index = 0
            for bullet in self.enemy_wavy_bullet_list:
                if self.reticle_rect.colliderect(bullet["rect"]):
                    enemy_bullets.wavy_bullet_list[bullet_index]["decay"] = 0
                    self.sheild_screen_shake_timer = self.sheild_screen_shake_max
                    break
                bullet_index += 1
    def reset(self):
       #States - store functions to go to, start and then normal
        self.states = {
                        "Normal":[self.normal_start,self.normal],
                        "Jumping":[self.jumping_start,self.jumping],
                        "Dead":[None,self.dead]
                        }
        self.state = self.states["Normal"]
        self.next_state = self.states["Normal"]
        #General Attributes
        self.x = self.start_x
        self.y = self.start_y
        self.hsp = 0
        self.vsp = 0
        self.image = pygame.image.load("Images/Player/trunkman_1.png").convert_alpha()
        self.dir_facing = 1
        self.rect = pygame.image.load("Images/Player/player_hitbox.png").get_rect()
        self.rect.x,self.rect.y = self.x,self.y
        self.hurtbox = pygame.image.load("Images/Player/player_hurtbox.png").get_rect()
        self.hurtbox.center = self.rect.center
        self.mask = pygame.mask.from_surface(pygame.image.load("Images/Player/player_hitbox.png")) #For slope collision
        self.sub_pixel_hsp = 0 #Helps with storing sub pixels
        self.sub_pixel_vsp = 0
        self.health = 4
        #Animations
        self.idle_animation = [[pygame.image.load("Images/Player/trunkman_1.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_2.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_3.png").convert_alpha(),5],
                               ]
        self.walk_animation = [[pygame.image.load("Images/Player/trunkman_walk_1.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_2.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_3.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_4.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_5.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_6.png").convert_alpha(),2],
                               [pygame.image.load("Images/Player/trunkman_walk_7.png").convert_alpha(),2]
                               ]
        self.jump_animation = [[pygame.image.load("Images/Player/trunkman_jump_1.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_jump_2.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_jump_3.png").convert_alpha(),5],
                               ]
        self.fall_animation = [[pygame.image.load("Images/Player/trunkman_fall_1.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_fall_2.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_fall_3.png").convert_alpha(),5],
                               ]      
        self.dash_animation = [[pygame.image.load("Images/Player/trunkman_dash_1.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_dash_2.png").convert_alpha(),5],
                               [pygame.image.load("Images/Player/trunkman_dash_3.png").convert_alpha(),5],
                               ]
        self.animation = self.walk_animation
        self.current_frame = [0,0]
        #UI
        self.low_health_face_animation = [[pygame.image.load("Images/UI/low_health_face_1.png").convert_alpha(),5],
                                          [pygame.image.load("Images/UI/low_health_face_2.png").convert_alpha(),5],
                                          [pygame.image.load("Images/UI/low_health_face_3.png").convert_alpha(),5],
                                          ]
        self.medium_health_face_animation = [[pygame.image.load("Images/UI/medium_health_face_1.png").convert_alpha(),5],
                                             [pygame.image.load("Images/UI/medium_health_face_2.png").convert_alpha(),5],
                                             [pygame.image.load("Images/UI/medium_health_face_3.png").convert_alpha(),5],
                                             ]
        self.good_health_face_animation = [[pygame.image.load("Images/UI/good_health_face_1.png").convert_alpha(),5],
                                             [pygame.image.load("Images/UI/good_health_face_2.png").convert_alpha(),5],
                                             [pygame.image.load("Images/UI/good_health_face_3.png").convert_alpha(),5],
                                             ]
        self.high_health_face_animation = [[pygame.image.load("Images/UI/high_health_face_1.png").convert_alpha(),5],
                                           [pygame.image.load("Images/UI/high_health_face_2.png").convert_alpha(),5],
                                           [pygame.image.load("Images/UI/high_health_face_3.png").convert_alpha(),5],
                                           ]
        self.health_face_animation = self.high_health_face_animation
        self.health_face_current_frame = [0,0]
        self.trunk_heart_animation = [[pygame.image.load("Images/UI/trunk_heart_1.png").convert_alpha(),5],
                                      [pygame.image.load("Images/UI/trunk_heart_2.png").convert_alpha(),5],
                                      [pygame.image.load("Images/UI/trunk_heart_3.png").convert_alpha(),5],
                                      ]
        self.trunk_heart_current_frame = [0,0]
        #Shooting
        self.bullet_animation = [[pygame.image.load("Images/Player/player_bullet_1.png").convert_alpha(),5],[pygame.image.load("Images/Player/player_bullet_2.png").convert_alpha(),5],[pygame.image.load("Images/Player/player_bullet_3.png").convert_alpha(),5]]
        self.charge_bullet_animation = [[pygame.image.load("Images/Player/player_charge_bullet_1.png").convert_alpha(),5]]
        self.shoot_bullet_timer = 0
        self.shoot_bullet_max = 10
        self.charge_bullet_timer = 0
        self.charge_bullet_max = 50
        self.bullet_speed = 10
        self.bullet_decay = 24 #How long bullet lasts
        self.bullet_rect_width = 12 #For making bullet rects
        self.bullet_rect_height = 12
        self.charge_bullet_rect_width = 32
        self.charge_bullet_rect_height = 32
        self.charge_bullet_damage = 3
        self.bullet_mask = pygame.mask.from_surface(pygame.image.load("Images/Player/player_bullet_1.png"))
        #Pointer
        self.pointer_animation = [[pygame.image.load("Images/Player/pointer_1.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_2.png").convert_alpha(),5],
                                  [pygame.image.load("Images/Player/pointer_3.png").convert_alpha(),5],
                                  ] 
        self.pointer_sheild_off_animation = [[pygame.image.load("Images/Player/pointer_sheild_off_1.png").convert_alpha(),5],
                                             [pygame.image.load("Images/Player/pointer_sheild_off_2.png").convert_alpha(),5],
                                             [pygame.image.load("Images/Player/pointer_sheild_off_3.png").convert_alpha(),5],
                                             ] 
        self.current_pointer_animation = self.pointer_animation
        self.pointer_rect = self.pointer_animation[0][0].get_rect() #Just for centering it
        self.pointer_current_frame = [0,0]
        #Reticle
        self.reticle_image = pygame.image.load("Images/Player/reticle.png").convert_alpha()
        self.charge_reticle_image = pygame.image.load("Images/Player/charge_reticle.png").convert_alpha()
        self.reticle_sheild_off_image = pygame.image.load("Images/Player/reticle_sheild_off.png").convert_alpha()
        self.charge_reticle_sheild_off_image = pygame.image.load("Images/Player/charge_reticle_sheild_off.png").convert_alpha()
        self.shooting_reticle_rect = pygame.image.load("Images/Player/reticle.png").get_rect()
        self.sheild_rect = pygame.image.load("Images/Player/sheild.png").get_rect()
        self.reticle_rect = pygame.image.load("Images/Player/reticle.png").get_rect() #So can blit reticle by centre
        self.reticle_distance_from_player = 30
        self.aiming_vector = pygame.Vector2(0,-1).normalize()  #For controller which doesn't start with input
        self.aiming_angle = 0
        #Sheild
        self.sheild_normal_image = pygame.image.load("Images/Player/sheild.png").convert_alpha()
        self.sheild__high_image= pygame.image.load("Images/Player/sheild_high.png").convert_alpha()
        self.sheild_med_image = pygame.image.load("Images/Player/sheild_med.png").convert_alpha()
        self.sheild_low_image = pygame.image.load("Images/Player/sheild_low.png").convert_alpha()
        self.sheild_image = self.sheild_normal_image
        self.sheild_on = True
        self.sheild_charged = True
        self.sheild_timer = 0
        self.sheild_max = 130
        #Effects
        #[x,y,current_frame]
        self.jump_effect_animation = [[pygame.image.load("Images/Player/jump_effect_1.png").convert_alpha(),2],
                                      [pygame.image.load("Images/Player/jump_effect_2.png").convert_alpha(),2],
                                      [pygame.image.load("Images/Player/jump_effect_3.png",).convert_alpha(),2],
                                      [pygame.image.load("Images/Player/jump_effect_4.png").convert_alpha(),2],
                                      ]
        self.jump_effect_list = []
        self.dash_effect_animation = [[pygame.image.load("Images/Player/dash_effect_1.png").convert_alpha(),2],
                                      [pygame.image.load("Images/Player/dash_effect_2.png").convert_alpha(),2],
                                      [pygame.image.load("Images/Player/dash_effect_3.png",).convert_alpha(),2],
                                      [pygame.image.load("Images/Player/dash_effect_4.png").convert_alpha(),2],
                                      [pygame.image.load("Images/Player/dash_effect_5.png").convert_alpha(),2],
                                      ]
        self.dash_effect_list = []
        #Inputs
        self.controller = False
        self.shooting_key = False
        self.sheild_key = False
        self.aiming_input = None
        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.jump_key_down = False
        self.jump_key_up = False
        self.dash_key = False
        self.pause_key = False
        #Collision Lists
        #Tiles
        self.solid_rect_list = []
        self.hazard_rect_list = []
        self.jump_through_platform_rect_list = []
        self.slope_rect_list = []
        self.enemy_solid_rect_list = []
        #Slopes
        self.slope_mask_list = []
        #Intances
        self.enemy_list = []
        #Bullets
        self.enemy_bullet_list = []
        self.enemy_lobber_list = []
        self.enemy_wavy_bullet_list = []
        #Dash
        self.dash_hdistance = 6
        self.dash_vdistance = 8
        self.dash_count = 0
        #All states
        self.grounded = False
        self.jump_buffer_max = 10
        self.jump_buffer_timer = self.jump_buffer_max
        self.coyote_jump_max = 10
        self.coyote_jump_timer = self.coyote_jump_max
        self.grv = 0.4
        self.max_grv = self.grv * 50
        #Invincibility Frames
        self.invincibility_max = 70
        self.invincibility_timer = self.invincibility_max
        self.invincibility_flash = True
        self.invincibility_flash_max = 4
        self.invincibility_flash_timer = self.invincibility_flash_max
        #Normal State
        self.normal_speed_max = 4
        self.normal_ground_acceleration = 0.5
        self.normal_ground_decceleration = self.normal_ground_acceleration * 5
        self.normal_ground_friction = 0.6
        self.normal_air_acceleration = 0.5
        self.normal_air_decceleration = self.normal_air_acceleration * 5
        self.normal_air_friction = 0.4
        #Jump State
        self.jump_height = -8
        self.hang_time_check = 0.5
        self.hang_time_multiplier = 0.5
        #Screen Shake 
        self.shooting_screen_shake_timer = 0
        self.shooting_screen_shake_max = 5
        self.sheild_screen_shake_timer = 0
        self.sheild_screen_shake_max = 5
        self.hurt_screen_shake_timer = 0
        self.hurt_screen_shake_max = 10
      
