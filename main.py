import pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# окно игры
W, H = 1920, 1080
screen = pygame.display.set_mode((W, H),flags=pygame.NOFRAME)
pygame.display.set_caption('ahhhhhhh')
clock = pygame.time.Clock()
FPS = 20
# иконка игры
icon = pygame.image.load('image/icon2.png').convert_alpha()
pygame.display.set_icon(icon)
# фон и музыка
bg = pygame.image.load('image/backfont1.jpg').convert()
bg_x = 0
start_bg = pygame.image.load('image/start_bg.png').convert_alpha()
bg_sound = pygame.mixer.Sound('sound/background.mp3')
bg_sound.play(loops=-1)
game_play_sound = pygame.mixer.Sound('sound/Rip_Tear.mp3')
game_play_sound.set_volume(0.5)
# параметры игрока
player_Stay = pygame.image.load('image/stay.png').convert_alpha()
player_step_sound = pygame.mixer.Sound('sound/step.mp3')
player_jump_sound = pygame.mixer.Sound('sound/jump.mp3')
player_caught_sound = pygame.mixer.Sound('sound/ahhhhhhh.mp3')
player_caught_sound.set_volume(1)
player_animation = 0
player_life = 10
player_life_reset = player_life
damage_from_ghost = 1
score= 0
dead_zone_L = 50
dead_zone_R = W - 50
player_x = 200
player_y = 900
jump_y = player_y
player_speed = 20
player_move = False
player_jump = False
player_not_jump = True
player_jump_speed = 40
player_jump_down = player_jump_speed / 2
jump_height = player_jump_speed * 6
player_jump_height = player_y - jump_height
player_moveL = [
    pygame.image.load('image/moveL.png').convert_alpha(),
    pygame.image.load('image/stay.png').convert_alpha()
]
player_moveR = [
    pygame.image.load('image/moveR.png').convert_alpha(),
    pygame.image.load('image/stay.png').convert_alpha()
]
player_JUMP = pygame.image.load('image/jump.png').convert_alpha()
player_jumpR = pygame.image.load('image/jumpR.png').convert_alpha()
player_jumpL = pygame.image.load('image/jumpL.png').convert_alpha()
player_shootR = pygame.image.load('image/shootR.png').convert_alpha()
player_shootL = pygame.image.load('image/shootL.png').convert_alpha()
player_jumpR_shoot = pygame.image.load('image/jumpR_shoot.png').convert_alpha()
player_jumpL_shoot = pygame.image.load('image/jumpL_shoot.png').convert_alpha()
# параметры призраков
ghost = pygame.image.load('image/ghost.png').convert_alpha()
ghost2 = pygame.image.load('image/ghost.png').convert_alpha()
ghost_list = []
ghost2_list = []
ghost_x = W + 100
ghost_y = H - 180
ghost2_x = -100
ghost2_y = H - 180
ghost_speed = 20
ghost2_speed = 15
ghost_time = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_time, 3000)
# параметры пуль
bulet = pygame.image.load('image/bulet.png').convert_alpha()
ammo_png = pygame.image.load('image/ammo.png').convert_alpha()
shoot_sound = pygame.mixer.Sound('sound/shoot.mp3')
reload_sound = pygame.mixer.Sound('sound/reload.mp3')
bulet_speed = 40
bulet_range = 1000
ammo = 10
ammo_add = 1
ammo_reset = ammo
ammo_x = W / 2
ammo_y = - 50
ammo_drop_speed = 20
ammo_drop_speed_reset = ammo_drop_speed
ammo_reload = []
bulets_R = []
bulets_L = []
# всякий текст
game_text = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
game_text_lose = game_text.render('you LOSE', False, (255,255,255))
game_text_restart = game_text.render('press SPACE to restart', False, (255,255,255))
game_text_exit = game_text.render('or ESC to exit', False, (255,255,255))
game_text_start = game_text.render('press SPACE to start', False, (255,255,255))
game_text_start_info1 = game_text.render('move LEFT press A',False, (255,255,255))
game_text_start_info2 = game_text.render('move RIGHT press D',False, (255,255,255))
game_text_start_info3 = game_text.render('JUMP press SPACE',False, (255,255,255))
game_text_start_info4 = game_text.render('SHOOT left press Q',False, (255,255,255))
game_text_start_info5 = game_text.render('SHOOT right press E',False, (255,255,255))
game_text_start_info6 = game_text.render('press ESC to EXIT',False, (255,255,255))
game_text_start_rect = game_text_start.get_rect(topleft=(W/2-200,H/2-100))
# условия для игры
startscrean =True
runTime = True
while runTime:   
    pygame.display.update()
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x + W,0))
    screen.blit(bg,(bg_x - W,0))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()   
    # стартовое окно
    if startscrean:
        screen.blit(game_text_start,(W/2-200,H/2-100))
        screen.blit(game_text_start_info1,(50,50))
        screen.blit(game_text_start_info2,(50,100))
        screen.blit(game_text_start_info3,(50,150))
        screen.blit(game_text_start_info4,(50,200))
        screen.blit(game_text_start_info5,(50,250))
        screen.blit(game_text_start_info6,(50,300))
        gameplay = False
        if keys[pygame.K_SPACE]:
            startscrean = False
            gameplay = True
            player_y = 500
            bg_sound.stop()
            game_play_sound.play(loops=-1)
        if keys[pygame.K_ESCAPE]:
            runTime = False
        if game_text_start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            startscrean = False
            gameplay = True
            player_y = 500
    else:
        # сам геймплей:
        if gameplay:
            player_rect = player_Stay.get_rect(topleft=(player_x,player_y))
            game_text_live = game_text.render('HP : ' + str(player_life), False, (255,255,255))
            game_text_ammo = game_text.render('AMMO : ' + str(ammo), False, (255,255,255))
            game_text_score = game_text.render('score: ' + str(score), False, (255,255,255))
            screen.blit(game_text_live,(50,50))
            screen.blit(game_text_ammo,(50,100))
            screen.blit(game_text_score,(W-300,50))
            # призраки:
            if ghost_list:
                for (i, el) in enumerate(ghost_list):
                    screen.blit(ghost, el)
                    el.x -= ghost_speed
                    if el.x < -50:
                        ghost_list.pop(i)
                    if player_rect.colliderect(el):
                        player_step_sound.stop()
                        player_caught_sound.play()
                        ghost_list.pop(i)
                        player_x = 200
                        player_y = 500
                        player_jump = False
                        player_life -= damage_from_ghost
                        if player_life == 0:
                            gameplay = False
                            bg_sound.play()
                            game_play_sound.stop()
            if ghost2_list:
                for (i, el) in enumerate(ghost2_list):
                    screen.blit(ghost2, el)
                    el.x += ghost2_speed
                    if el.x > W + 50:
                        ghost2_list.pop(i)
                    if player_rect.colliderect(el):
                        player_step_sound.stop()
                        player_caught_sound.play()
                        ghost2_list.pop(i)
                        player_x = 200
                        player_y = 500
                        player_jump = False
                        player_life -= damage_from_ghost
                        if player_life == 0:
                            gameplay = False
                            bg_sound.play()
                            game_play_sound.stop()
            # перезарядка
            if ammo_reload:
                for (i, el) in enumerate(ammo_reload):
                    screen.blit(ammo_png, el)
                    el.y += ammo_drop_speed
                    if el.y > H -180:
                        ammo_drop_speed = 0
                    if el.y > H + 100:
                        ammo_reload.pop(i)
                    if player_rect.colliderect(el):
                        ammo_reload.clear()
                        if ammo < 10:
                            ammo += ammo_add
                            ammo_drop_speed = ammo_drop_speed_reset
                            player_step_sound.stop()
                            reload_sound.play()
            # анимация:
            if player_animation == 1:
                player_animation = 0
            else:
                player_animation += 1
            if keys[pygame.K_q] and ammo > 0:
                screen.blit(player_shootL,(player_x,player_y))
            elif keys[pygame.K_e] and ammo > 0:
                screen.blit(player_shootR,(player_x,player_y))
            elif keys[pygame.K_a] and player_not_jump:
                screen.blit(player_moveL[player_animation],(player_x,player_y))
            elif keys[pygame.K_d] and player_not_jump:
                screen.blit(player_moveR[player_animation],(player_x,player_y))
            elif not player_not_jump:
                if keys[pygame.K_a]:
                    screen.blit(player_jumpL,(player_x,player_y))
                elif keys[pygame.K_d]:
                    screen.blit(player_jumpR,(player_x,player_y))
                elif keys[pygame.K_q] and ammo > 0:
                    screen.blit(player_jumpL_shoot,(player_x,player_y))
                elif keys[pygame.K_e] and ammo > 0:
                    screen.blit(player_jumpR_shoot,(player_x,player_y))
                else:
                    screen.blit(player_JUMP,(player_x,player_y))
            else:
                screen.blit(player_Stay,(player_x,player_y))
            # передвижение и двигаем фон:
            if keys[pygame.K_a]:
                if player_not_jump:
                    player_step_sound.play()
                if player_x > dead_zone_L:
                    player_x -= player_speed
                bg_x += 2
                if bg == +3840:
                    bg_x = 0
            elif keys[pygame.K_d]:
                if player_not_jump:
                    player_step_sound.play()
                if player_x < dead_zone_R:
                    player_x += player_speed
                bg_x -= 2
                if bg == -3840:
                    bg_x = 0
            # прыжок:
            if keys[pygame.K_SPACE] and player_y == jump_y:
                player_step_sound.stop()
                player_jump_sound.play()
                player_jump = True
            if player_jump == True:
                player_y -= player_jump_speed
                if player_y == player_jump_height:
                    player_jump = False
            elif player_y < jump_y:
                player_y += player_jump_down
            if player_y == jump_y:
                player_not_jump = True
            else:
                player_not_jump = False
            # пули:
            if bulets_R:
                for (i, el) in enumerate(bulets_R):
                    screen.blit(bulet, (el.x, el.y))
                    el.x += bulet_speed   
                    if el.x > player_x + bulet_range:
                        bulets_R.pop(i)       
                    if ghost_list:
                        for (index, ghost_el) in  enumerate(ghost_list):
                            if el.colliderect(ghost_el):
                                ghost_list.pop(index)
                                bulets_R.pop(i)
                                score += 1
                                player_step_sound.stop()
                                player_caught_sound.play()
                    if ghost2_list:
                        for (index, ghost2_el) in  enumerate(ghost2_list):
                            if el.colliderect(ghost2_el):
                                ghost2_list.pop(index)
                                bulets_R.pop(i)
                                score += 1
                                player_step_sound.stop()
                                player_caught_sound.play()
            if bulets_L:
                for (i, el) in enumerate(bulets_L):
                    screen.blit(bulet, (el.x, el.y))
                    el.x -= bulet_speed   
                    if el.x < player_x - bulet_range:
                        bulets_L.pop(i)          
                    if ghost_list:
                        for (index, ghost_el) in  enumerate(ghost_list):
                            if el.colliderect(ghost_el):
                                ghost_list.pop(index)
                                bulets_L.pop(i)
                                score += 1
                                player_step_sound.stop()
                                player_caught_sound.play()
                    if ghost2_list:
                        for (index, ghost2_el) in  enumerate(ghost2_list):
                            if el.colliderect(ghost2_el):
                                ghost2_list.pop(index)
                                bulets_L.pop(i)
                                score += 1
                                player_step_sound.stop()
                                player_caught_sound.play()                               
        # LOSE screan
        else:
            screen.blit(game_text_lose, (W/2-80,H/2-150))
            screen.blit(game_text_restart, (W/2-200,H/2-100))
            screen.blit(game_text_exit, (W/2-110,H/2-50))
            if keys[pygame.K_SPACE]:
                gameplay = True
                player_life = player_life_reset
                ammo = ammo_reset
                score = 0
                ghost_list.clear()
                ghost2_list.clear()
                bulets_R.clear()
                bulets_L.clear()
                ammo_reload.clear()
                game_play_sound.play()
            if keys[pygame.K_ESCAPE]:
                runTime = False
    # обработчик событий 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            runTime = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                runTime = False
        if event.type == ghost_time:
            ghost_list.append(ghost.get_rect(topleft=(ghost_x,player_y)))
            ghost2_list.append(ghost2.get_rect(topleft=(ghost2_x,ghost2_y)))
            ammo_reload.append(ammo_png.get_rect(topleft=(player_x,ammo_y)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_e and ammo > 0:
            bulets_R.append(bulet.get_rect(topleft=(player_x + 40,player_y + 30)))
            ammo -= 1
            player_step_sound.stop()
            shoot_sound.play()
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_q and ammo > 0:
            bulets_L.append(bulet.get_rect(topleft=(player_x - 40,player_y + 30)))
            ammo -= 1
            player_step_sound.stop()
            shoot_sound.play()
    clock.tick(FPS)