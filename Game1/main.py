import pygame
from random import randint, choice
from sys import exit
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()

        self.player_index = 0
        self.player_walk = [player_walk_1, player_walk_2]
        self.image = self.player_walk[self.player_index]

        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load(
                'graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load(
                'graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = score_font.render(
        f'score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def instruction_to_start_game(score):
    title_surface = score_font.render(
        f'Runer Game!', False, (111, 196, 169))
    title_rectangle = title_surface.get_rect(center=(400, 80))

    instruction_surface = score_font.render(
        f'Hit Space to start game!', False, (111, 196, 169))
    instruction_rectangle = title_surface.get_rect(center=(310, 340))

    score_message = score_font.render(
        f'Your score: {score}', False, (111, 196, 169))
    score_message_rect = score_message.get_rect(center=(400, 330))
    if score == 0:
        screen.blit(instruction_surface, instruction_rectangle)
    else:
        screen.blit(score_message, score_message_rect)
    screen.blit(title_surface, title_rectangle)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


def player_animation():
    global player_index, player_surface
    """
    play walking animation if player is on the floor
    display the jump surface if player is not on the floor
    """
    if player_rectangle.bottom < 300:
        # jump animation
        player_surface = player_jump
    else:
        # walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


score = 0
start_time = 0
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)

background_music = pygame.mixer.Sound('audio/music.wav')
background_music.play(loops=-1)
# Groups

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
score_surface = score_font.render('My Game', False, (64, 64, 64))
# obstacles
obstacles_rect_list = []
# fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]

fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

# snail
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]

snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

score_rectange = score_surface.get_rect(center=(400, 50))

# player walk
player_walk_1 = pygame.image.load(
    'graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_index = 0
player_walk = [player_walk_1, player_walk_2]
player_surface = player_walk[player_index]

player_rectangle = player_surface.get_rect(midbottom=(80, 300))
# snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))
player_gravity = 0


game_active = False

# Intro Screen
player_stand = pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))
# print(image.get_size())
# test_surface.fill('red')

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# snail animation timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

# fly animation timer

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # snail_rectangle.left = 800
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'snail', 'snail', 'snail', 'snail''fly', 'fly'])))

                # if randint(0, 1):
                #     obstacles_rect_list.append(snail_surface.get_rect(
                #         midbottom=(randint(900, 1100), 300)))
                # else:
                #     obstacles_rect_list.append(fly_surface.get_rect(
                #         midbottom=(randint(900, 1100), 210)))
        # if event.type == pygame.KEYUP:
        #     print('key Up ')
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    # draw the elements and update

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rectange)
        # pygame.draw.rect(screen, '#c0e8ec', score_rectange, 30)
        score = display_score()
        # pygame.draw.line(screen, 'gold', (0, 0), pygame.mouse.get_pos(), 12)
        # screen.blit(score_surface, score_rectange)
        # snail_rectangle.x -= 1
        # if snail_rectangle.right <= 0:
        #     snail_rectangle.left = 800

        # screen.blit(snail_surface, snail_rectangle)
        # Player
        # player_gravity += 1
        # player_rectangle.y += player_gravity
        # if player_rectangle.bottom >= 300:
        #     player_rectangle.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rectangle)

        # obstacle movement

        # obstacles_rect_list = obstacle_movement(obstacles_rect_list)

        # keys = pygame.key.get_pressed()

        # if (player_rectangle.colliderect(snail_rectangle)):
        # mouse_poition = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_poition):
        #     print(pygame.mouse.get_pressed())

        # coliision
        # game_active = collisions(player_rectangle, obstacles_rect_list)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

        # if snail_rectangle.colliderect(player_rectangle):
        #     game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacles_rect_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0
        instruction_to_start_game(score)

    pygame.display.update()
    clock.tick(60)
