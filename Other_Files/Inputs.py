from General_Functions import *

"""
Returns dict of inputs, manages controller support
"""

#Inputs, returns input_dict
def inputs(controller):
    input_dict = {
            "controller":False,
            "mouse_pos":None,
            "left_click_down":None,
            "aiming_input":None,
            "shooting_key":False,
            "shooting_key_down":False,
            "sheild_key":False,
            "left_key":0,
            "right_key":0,
            "down_key":0,
            "jump_key_down":False,
            "jump_key_up":False,
            "dash_key":False,
            "pause_key":False
        }
    #Check for controller
    controller_amount = pygame.joystick.get_count()
    if controller_amount != 0:
        input_dict["controller"] = True
        if not controller:
            try:
                controller = pygame.joystick.Joystick(0)
            except:
                controller = False
    else:
        controller = False
    if controller:
        controller_name = controller.get_name()
    #Event Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                input_dict["left_click_down"] = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                input_dict["pause_key"] = True
        #No Controller
        if input_dict["controller"] == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    input_dict["jump_key_down"] = True
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT or event.key == pygame.K_RCTRL:
                    input_dict["dash_key"] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    input_dict["shooting_key_down"] = True
        #Controller
        else:
            if controller_name[:4] == "Xbox":
                if event.type == pygame.JOYBUTTONDOWN:
                    if controller_name[:4] == "Xbox":
                        if event.button == 0 or event.button == 5:
                            input_dict["jump_key_down"] = True
                        if event.button == 1 or event.button == 4:
                            input_dict["dash_key"] = True
                        if event.button == 7:
                            input_dict["pause_key"] = True
            elif controller_name[:2] == "PS":
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 or event.button == 10:
                        input_dict["jump_key_down"] = True
                    if event.button == 1 or event.button == 9:
                        input_dict["dash_key"] = True
                    if event.button == 6:
                        input_dict["pause_key"] = True
    #State Inputs
    input_dict["mouse_pos"] = pygame.mouse.get_pos()  
    #No Controller
    if input_dict["controller"] == False:
        input_dict["aiming_input"] = pygame.mouse.get_pos()  
        mouse_keys_pressed = pygame.mouse.get_pressed()
        keys_pressed = pygame.key.get_pressed()
        if mouse_keys_pressed[0]:
            input_dict["shooting_key"] = True
        if mouse_keys_pressed[2] or keys_pressed[pygame.K_LALT] or keys_pressed[pygame.K_RALT]:
            input_dict["sheild_key"] = True
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            input_dict["left_key"] = 1
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            input_dict["right_key"] = 1
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            input_dict["down_key"] = 1
        if not keys_pressed[pygame.K_SPACE] and not keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_UP]:
            input_dict["jump_key_up"] = True
    #Controller
    else:
        input_dict["aiming_input"] = [0,0]
        controller_aiming_vector = pygame.Vector2(controller.get_axis(3),controller.get_axis(4))
        #Xbox
        if controller_name[:4] == "Xbox":
            if controller.get_axis(2) != -1:
                input_dict["sheild_key"] = True
            if controller.get_axis(5) != -1:
                input_dict["shooting_key"] = True
            if controller.get_axis(0) <= -0.5:
                input_dict["left_key"] = int(True)
            elif controller.get_axis(0) >= 0.5:
                input_dict["right_key"] = int(True)
            else:
                if controller.get_hat(0)[0] == -1:
                    input_dict["left_key"] = int(True)
                elif controller.get_hat(0)[0] == 1:
                    input_dict["right_key"] = int(True)
            if controller.get_axis(1) >= 0.5:
                input_dict["down_key"] = int(True)
            else:
                if controller.get_hat(0)[1] == -1:
                    input_dict["down_key"] = int(True)
            if not controller.get_button(0) and not controller.get_button(5):
                input_dict["jump_key_up"] = True
        #PS4
        elif controller_name[:2] == "PS":
            if controller.get_axis(4) != -1:
                input_dict["sheild_key"] = True
            if controller.get_axis(5) != -1:
                input_dict["shooting_key"] = True
            if controller.get_axis(0) <= -0.5:
                input_dict["left_key"] = int(True)
            elif controller.get_axis(0) >= 0.5:
                input_dict["right_key"] = int(True)
            else:
                if controller.get_button[13] == -1:
                    input_dict["left_key"] = int(True)
                elif controller.get_button[14] == 1:
                    input_dict["right_key"] = int(True)
            if not controller.get_button(0) and not controller.get_button(10):
                input_dict["jump_key_up"] = True
            if controller.get_axis(1) >= 0.5:
                input_dict["down_key"] = int(True)
            else:
                if controller.get_button(13) == -1:
                    input_dict["down_key"] = int(True)
        if controller_aiming_vector.length() >= 0.5 or controller_aiming_vector.length() <= -0.5:
            input_dict["aiming_input"] = [controller.get_axis(3),controller.get_axis(4)]
    return input_dict, controller
