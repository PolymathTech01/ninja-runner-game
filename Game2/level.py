import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        self.player_on_ground = False
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.player.add(
                        Player((x, y), self.display_surface, self.create_jump_particles))

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(
                self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        # direction_X will be -1 when player is moving to the left and will be 1 when player is moving to the right
        if player_x < (screen_width / 4) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    # when the player is going out of the collided rectangle
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                # player.rect.left < self.current_x -- means the player exceeded the tiles and is not touching the tiles anymore
                # Another case is if a player is touching the wall on the left, it is perfectly possible that he is trying to move to the right and it will stop touching the left wall so we have player.direction >= 0
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            # the player is already on the ground
            # this checking as the player.on_ground is set to true, is the player falling or jumping
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            # the player is already on the ceiling, this is cheking as player.on_ceiling is set to true, and is the player jumping
            player.on_ceiling = False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particles_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particles_sprite)

    def run(self):
        # dust particles

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # level tiles

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player

        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
