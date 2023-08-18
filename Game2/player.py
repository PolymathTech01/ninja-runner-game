import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles) -> None:
        super().__init__()
        self.import_character_assests()
        # self.image = pygame.Surface((32, 64))
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        self.create_jump_particles = create_jump_particles
        # player status

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assests(self):
        character_path = './Game2/assets/graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder(
            './Game2/assets/graphics/character/dust_particles/run')

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
        else:
            self.direction.x = 0

    def animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            # player is on the ground and colliding with the right wall
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            # self.rect.bottomright is the positon of the previous rectangle
        elif self.on_ground and self.on_left:
            # player is on the ground and colliding with the left wall
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        elif self.on_ceiling and self.on_right:
            # player is on the ceiling and colliding with the right wall
            self.rect = self.image.get_rect(topright=self.rect.topright)
            # self.rect.topright is the positon of the previous rectangle
        elif self.on_ceiling and self.on_left:
            # player is on the ceiling and colliding with the left wall
            self.rect = self.image.get_rect(topleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(topleft=self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0.9:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
