from General_Functions import *

class Game_State_Manager():
    """
    Manages state, is a way to get everything to update which is dependent on other things without using 
    global variables.
    Should be used when adding menus, etc
    """
    def __init__(self):
        self.states = { 
                            "Normal":"Normal",
                            "Pause":"Pause",
                            "Dead":"Dead",
                            "Reset Level":"Reset Level",
                            "Menu":"Menu",
                            "Start Screens":"Start Screens",
                            "Start Game":"Start Game",
                            "Intro Cutscene":"Intro Cutscene",
                            "Ending Cutscene":"Ending Cutscene"
                        }
        self.state = self.states["Start Screens"]
        self.start_level = None
        self.surface = pygame.Surface(pygame.display.get_surface().get_size())
        self.all_enemies_dead = False
        #Start Screens
        self.start_screens_timer = 0
        self.logo_image = pygame.image.load("Images/UI/logo.png").convert()
        self.mouse_and_keyboard_image = pygame.image.load("Images/UI/keyboard_screen.png").convert()
    def update(self,input_dict,player,player_bullets,camera,tilemap,instances,enemy_bullets,menu,intro_cutscene,ending_cutscene,pause_menu,death_screen):
        if self.state == self.states["Normal"]:
            player.update(self,input_dict,tilemap,instances,enemy_bullets,death_screen)
            player.update_shooting(camera,player_bullets)
            player_bullets.update(tilemap)
            camera.follow(player,tilemap.level_width,tilemap.level_height)
            tilemap.update(camera)
            instances.update(tilemap,enemy_bullets,player_bullets,player.rect.centerx,player.rect.centery,[player.sheild_on,player.reticle_rect],player.aiming_vector)
            enemy_bullets.update(tilemap)
            #Check if all enemies are dead
            self.all_enemies_dead = True
            for enemy in instances.instance_dict["enemy_list"]:
                if enemy.state != enemy.states["Dead"]:
                    self.all_enemies_dead = False
                    break
            if self.all_enemies_dead:
                goal_collision_check = player.rect.collidedictall(tilemap.tile_rect_dict["goal_rect_dict"])
                if goal_collision_check:
                    goal_rect_index = goal_collision_check[0][0]
                    level_to_go_to = tilemap.tile_rect_dict["goal_rect_dict"][goal_rect_index]
                    player_bullets.reset()
                    enemy_bullets.reset()
                    print("hello",level_to_go_to)
                    #Ending Cutscene
                    if level_to_go_to == "Levels/end":
                        self.state = self.states["Ending Cutscene"]
                    #Autosave
                    else:
                        save_file_dict = json.load(open("Save/save.json","r"))
                        save_file_dict["start_level"] = level_to_go_to
                        self.load_new_level(level_to_go_to,player,camera,tilemap,instances)
                        save_file = open("Save/save.json","w")
                        json.dump(save_file_dict,save_file)
                        save_file.close()
        elif self.state == self.states["Pause"]:
            pause_menu.update(self,input_dict,tilemap.level_name)
        elif self.state == self.states["Dead"]:
            death_screen.update(self,input_dict)        
        elif self.state == self.states["Reset Level"]:
            instances.reset()
            player.reset()
            player_bullets.reset()
            enemy_bullets.reset()
            camera.reset(camera.start_x,camera.start_y)
            self.state = self.states["Normal"]
        elif self.state == self.states["Menu"]:
            menu.update(self,input_dict)
        elif self.state == self.states["Start Screens"]:
            self.start_screens_timer += 1
        elif self.state == self.states["Start Game"]:
            save_file = json.load(open("Save/save.json","r"))
            #If intro hasn't been played before
            if save_file["intro_played"] == False:
                self.state = self.states["Intro Cutscene"]
            else:
                self.start_level = save_file["start_level"]
                self.load_new_level(self.start_level,player,camera,tilemap,instances)
                enemy_bullets.reset()
                self.state = self.states["Normal"]
        elif self.state == self.states["Intro Cutscene"]:
            intro_cutscene.update(self,input_dict)
        elif self.state == self.states["Ending Cutscene"]:
            ending_cutscene.update(self,input_dict)
    def draw(self,screen,player,player_bullets,camera,tilemap,instances,enemy_bullets,menu,intro_cutscene,ending_cutscene,pause_menu,death_screen):
        if self.state == self.states["Normal"]:
            tilemap.draw_background(self.surface,camera)
            instances.draw_behind(self.surface,camera)
            tilemap.draw_goal(self.surface,self.all_enemies_dead,camera)
            player.draw(self.surface,camera)
            instances.draw(self.surface,camera)
            tilemap.draw(self.surface,camera)
            enemy_bullets.draw(self.surface,camera)
            player_bullets.draw(self.surface,camera)
            player.draw_aiming_reticle(self.surface,camera)
            tilemap.draw_ui(self.surface,camera)
            #Screen Shake
            if player.hurt_screen_shake_timer > 0:
                screen.blit(self.surface,(random.uniform(-4,4),random.uniform(-5,5)))
            elif instances.bounce_screen_shake_check():
                screen.blit(self.surface,(random.uniform(-4,4),random.uniform(-4,4)))
            elif player.sheild_screen_shake_timer > 0:
                screen.blit(self.surface,(random.uniform(-4,4),random.uniform(-4,4)))
            else:
                screen.blit(self.surface,(0,0))
            """
            elif player.shooting_screen_shake_timer > 0:
                screen.blit(self.surface,(random.uniform(-2,2),random.uniform(-2,2)))
            """
        elif self.state == self.states["Dead"]:
            death_screen.draw(screen)
        elif self.state == self.states["Menu"]:
            menu.draw(screen)
        elif self.state == self.states["Start Screens"]:
            if self.start_screens_timer >= 200:
                if self.start_screens_timer <= 250:
                    self.mouse_and_keyboard_image.set_alpha(((self.start_screens_timer-200)/50)*255)
                elif self.start_screens_timer >= 350:
                    self.mouse_and_keyboard_image.set_alpha(255-(((self.start_screens_timer-350)/50)*255))
                else:
                    self.mouse_and_keyboard_image.set_alpha(255)
                screen.fill((0,0,0))
                screen.blit(self.mouse_and_keyboard_image,(0,0))
            else:
                if self.start_screens_timer <= 50:
                    self.logo_image.set_alpha((self.start_screens_timer/50)*255)
                elif self.start_screens_timer >= 150:
                    self.logo_image.set_alpha(255-(((self.start_screens_timer-150)/50)*255))
                else:
                    self.logo_image.set_alpha(255)
                screen.fill((0,0,0))
                screen.blit(self.logo_image,(0,0))
            if self.start_screens_timer >= 400:
                self.state = self.states["Menu"]
        elif self.state == self.states["Pause"]:
            pause_menu.draw(screen)
        elif self.state == self.states["Intro Cutscene"]:
            intro_cutscene.draw(screen)
        elif self.state == self.states["Ending Cutscene"]:
            ending_cutscene.draw(screen)
    def load_new_level(self,level_name,player,camera,tilemap,instances):
        tilemap.level_name = level_name
        #Unlock Level
        level_name_split = level_name.split("/")
        level_path = ""
        print(level_name_split)
        for i in level_name_split[0:len(level_name_split)-1]:
            level_path += i + "/" 
        print(level_path)
        level_save_file = open(level_path+"save.json","r")
        temp = json.load(level_save_file).copy()
        temp["unlocked"] = True
        level_save_file.close()
        level_save_file = open(level_path+"save.json","w")
        json.dump(temp,level_save_file)
        level_save_file.close()
        #Level Name Image
        tilemap.level_name_animation[0][0] = pygame.image.load(level_path+"image_1.png").convert_alpha()
        tilemap.level_name_animation[1][0] = pygame.image.load(level_path+"image_2.png").convert_alpha()
        tilemap.level_name_animation[2][0] = pygame.image.load(level_path+"image_3.png").convert_alpha()
        #Load Level File
        level_data_file = open(level_name+"_data.csv","r")
        level_data_file_reader = csv.reader(level_data_file,delimiter = ",")
        tilemap.level_data_list = []
        for row in level_data_file_reader:
            tilemap.level_data_list.append(row)
        level_data_file.close()
        background_file = json.load(open(level_name+"_backgrounds.json","r"))
        tilemap.background_layer_1 = tilemap.background_dict[background_file["background_layer_1"]].copy()
        tilemap.background_layer_2 = tilemap.background_dict[background_file["background_layer_2"]].copy()
        tilemap.background_layer_3 = tilemap.background_dict[background_file["background_layer_3"]].copy()
        tilemap.bottom_layer = tilemap.background_dict[background_file["bottom_layer"]].copy()
        #Init Level
        instances.instance_dict = {
            "enemy_list":[],
            "decor_list":[],
            "decor_behind_list":[],
        }
        tilemap.tile_rect_dict = {
            "solid_rect_list":[],
            "hazard_rect_list":[],
            "jump_through_platform_rect_list":[],
            "slope_rect_list":[],
            "bullet_solid_rect_list":[],
            "enemy_solid_rect_list":[], #Solid's enemies and bullets can't go through
            "goal_rect_dict":{}
        }
        tilemap.slope_mask_list = []
        tilemap.level_width = len(tilemap.level_data_list[0])*tilemap.tile_width
        tilemap.level_height = len(tilemap.level_data_list)*tilemap.tile_height
        tilemap.tile_surface = pygame.Surface((tilemap.level_width,tilemap.level_height),pygame.SRCALPHA).convert_alpha()
        tilemap.back_tile_surface = pygame.Surface((tilemap.level_width,tilemap.level_height),pygame.SRCALPHA).convert_alpha()
        #self.tile_surface.fill((135,206,235))
        for row in range(len(tilemap.level_data_list)):
            for tile in range(len(tilemap.level_data_list[row])):
                #Player
                if tilemap.level_data_list[row][tile] == "player":
                    player.start_x = tile * tilemap.tile_width
                    player.start_y = row * tilemap.tile_height - 10
                    player.reset()
                #Instances
                elif tilemap.level_data_list[row][tile] == "monobrow_bug":
                    instances.add_instance("enemy_list","Monobrow_Bug",tile*tilemap.tile_width,row*tilemap.tile_height-3)
                elif tilemap.level_data_list[row][tile] == "mouth_stack":
                    instances.add_instance("enemy_list","Mouth_Stack",tile*tilemap.tile_width,row*tilemap.tile_height-96)
                elif tilemap.level_data_list[row][tile] == "beak_balloon":
                    instances.add_instance("enemy_list","Beak_Balloon",tile*tilemap.tile_width,row*tilemap.tile_height-32)
                elif tilemap.level_data_list[row][tile] == "jaw_cloud":
                    instances.add_instance("enemy_list","Jaw_Cloud",tile*tilemap.tile_width,row*tilemap.tile_height-32)
                elif tilemap.level_data_list[row][tile] == "cyclops_turret":
                    instances.add_instance("enemy_list","Cyclops_Turret",tile*tilemap.tile_width+35,row*tilemap.tile_height-44)
                elif tilemap.level_data_list[row][tile] == "winged_donut":
                    instances.add_instance("enemy_list","Winged_Donut",tile*tilemap.tile_width,row*tilemap.tile_height)
                elif tilemap.level_data_list[row][tile] == "donut":
                    instances.add_instance("enemy_list","Donut",tile*tilemap.tile_width,row*tilemap.tile_height)
                elif tilemap.level_data_list[row][tile] == "snout_slime":
                    instances.add_instance("enemy_list","Snout_Slime",tile*tilemap.tile_width,row*tilemap.tile_height-3)
                elif tilemap.level_data_list[row][tile] == "slug_bug":
                    instances.add_instance("enemy_list","Slug_Bug",tile*tilemap.tile_width,row*tilemap.tile_height-28)
                elif tilemap.level_data_list[row][tile] == "tap_bug":
                    instances.add_instance("enemy_list","Tap_Bug",tile*tilemap.tile_width,row*tilemap.tile_height+5)
                elif tilemap.level_data_list[row][tile] == "villiform_man":
                    instances.add_instance("enemy_list","Villiform_Man",tile*tilemap.tile_width,row*tilemap.tile_height-75)
                #Tiles
                elif tilemap.level_data_list[row][tile][0:5] == "solid":
                    tilemap.tile_rect_dict["solid_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][0:6] == "bullet":
                    tilemap.tile_rect_dict["bullet_solid_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][0:5] == "enemy":
                    tilemap.tile_rect_dict["enemy_solid_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile] == "hazard":
                    tilemap.tile_rect_dict["hazard_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][:21] == "jump_through_platform":
                    tilemap.tile_rect_dict["jump_through_platform_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,4))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][0:10] == "slope_left":
                    #Adds list with [mask,x,y]
                    tilemap.slope_mask_list.append([pygame.mask.from_surface(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png")),tile*tilemap.tile_width,row*tilemap.tile_height])
                    tilemap.tile_rect_dict["slope_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][0:11] == "slope_right":
                    #Adds list with [mask,x,y]
                    tilemap.slope_mask_list.append([pygame.mask.from_surface(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png")),tile*tilemap.tile_width,row*tilemap.tile_height])
                    tilemap.tile_rect_dict["slope_rect_list"].append(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height))
                    tilemap.tile_surface.blit(pygame.image.load("Images/Tilesets/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height))
                elif tilemap.level_data_list[row][tile][:4] == "goal":
                    #Appends dict with rect:level_to_go_to
                    tilemap.tile_rect_dict["goal_rect_dict"].update({tuple(pygame.Rect(tile*tilemap.tile_width,row*tilemap.tile_height,tilemap.tile_width,tilemap.tile_height)):"Levels/"+tilemap.level_data_list[row][tile][5:]})
                #Tutorial
                elif tilemap.level_data_list[row][tile][:8] == "tutorial":
                    tilemap.back_tile_surface.blit(pygame.image.load("Images/UI/"+tilemap.level_data_list[row][tile]+".png").convert_alpha(),(tile*tilemap.tile_width,row*tilemap.tile_height-68))
                #Decor
                elif tilemap.level_data_list[row][tile][:12] == "decor_behind":
                    instances.add_instance("decor_behind_list",tilemap.level_data_list[row][tile][13:],tile*tilemap.tile_width,row*tilemap.tile_height)
                elif tilemap.level_data_list[row][tile][:5] == "decor":
                    instances.add_instance("decor_list",tilemap.level_data_list[row][tile][6:],tile*tilemap.tile_width,row*tilemap.tile_height)
        #Camera
        camera_start_x = player.start_x - camera.screen_width/2
        camera_start_y = player.start_y - camera.screen_height/2
        camera_start_x = clamp(camera_start_x,0,tilemap.level_width - camera.screen_width)
        camera_start_y = clamp(camera_start_y,0,tilemap.level_height - camera.screen_height)
        camera.reset(camera_start_x,camera_start_y)
        tilemap.set_background_start_positions(camera_start_x,camera_start_y)

