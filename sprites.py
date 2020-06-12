# Sprite classes
import pygame as pg
import random
import math
from pygame import gfxdraw
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        # Initiate player sprite
        self.groups = game.all_sprites
        pg.sprite.Sprite. __init__(self, self.groups)
        self.game = game
        # Draw player image
        self.draw()
        # Initiate positional parameters
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.last_shot = 0

    def draw(self):
        self.original_image = pg.Surface((PLAYER_WIDTH + 2, PLAYER_HEIGHT + 2), pg.SRCALPHA)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        pg.draw.line(self.original_image, WHITE, (0, PLAYER_HEIGHT)
                                               , (PLAYER_WIDTH / 2, 0), 2)
        pg.draw.line(self.original_image, WHITE, (PLAYER_WIDTH, PLAYER_HEIGHT)
                                               , (PLAYER_WIDTH / 2, 0), 2)
        pg.draw.line(self.original_image, WHITE, (2, PLAYER_HEIGHT - (PLAYER_HEIGHT * 0.2))
                                               , (PLAYER_WIDTH-2, PLAYER_HEIGHT - (PLAYER_HEIGHT * 0.2)), 2)
        
    def controller(self):
        self.rot_speed = 0
        self.acc = vec(0, 0)
        # User input
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP]:
            self.acc = vec(0, -PLAYER_ACC).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(0, -1).rotate(-self.rot)
                pos = self.pos + vec(0 , -PLAYER_HEIGHT / 2).rotate(-self.rot)
                Bullet(self.game, pos, dir)
         
    def update(self):
        self.controller()
        # Sprite movement
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 
        self.image = pg.transform.rotate(self.original_image, self.rot)
        self.rect = self.image.get_rect(center = self.pos)
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc * self.game.dt
        # Screen wrapping
        if self.pos.x - PLAYER_WIDTH  > WIDTH:
            self.pos.x = 0 - PLAYER_WIDTH
        if self.pos.x + PLAYER_WIDTH < 0:
            self.pos.x = WIDTH + PLAYER_WIDTH
        if self.pos.y - PLAYER_HEIGHT > HEIGHT:
            self.pos.y = 0 - PLAYER_HEIGHT
        if self.pos.y + PLAYER_HEIGHT < 0:
            self.pos.y = HEIGHT + PLAYER_HEIGHT

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        # Initiate bullet sprite
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(pos)
        self.image = pg.Surface((BULLET_SIZE, BULLET_SIZE), pg.SRCALPHA)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED * self.game.dt
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        self.mask = pg.mask.from_surface(self.image)
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        
class Asteroid(pg.sprite.Sprite):
    def __init__(self, game, pos, asteroid_type):
        # Initiate asteroid sprite
        if asteroid_type == 'large':  
            self.groups = game.all_sprites, game.asteroids
            self.size = ASTEROID_MAX_RADIUS
            self.min_size = ASTEROID_MIN_RADIUS
            self.speed = random.uniform(1, ASTEROID_MAX_SPEED / 3)
        elif asteroid_type == 'medium': 
            self.groups = game.all_sprites, game.asteroids
            self.size = ASTEROID_MAX_RADIUS / 2
            self.speed = random.uniform(ASTEROID_MAX_SPEED / 3, ASTEROID_MAX_SPEED / 2)
            self.min_size = ASTEROID_MIN_RADIUS / 2
        else:
            self.groups = game.all_sprites, game.asteroids
            self.size = ASTEROID_MAX_RADIUS / 4
            self.speed = random.uniform(ASTEROID_MAX_SPEED / 2, ASTEROID_MAX_SPEED)
            self.min_size = ASTEROID_MIN_RADIUS / 4
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        # Initiate positional parameters
        self.pos = pos
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.asteroid_type = asteroid_type
        # Draw Asteroid image
        self.draw()

    def draw(self):
        self.image = pg.Surface((self.size * 2, self.size * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vertices = []
        ang = 0
        # Generate random vertices
        while ang < 2 * math.pi:
            self.vary = random.uniform(ASTEROID_MIN_VARY, ASTEROID_MAX_VARY)
            self.varyang = self.vary * (2 * math.pi / ASTEROID_GANULARITY)
            self.ang = ang + self.varyang - (math.pi / ASTEROID_GANULARITY) 
            self.radius = random.uniform(self.min_size, self.size)
            self.vertices.append((self.size + math.sin(self.ang) * self.radius
                                  , self.size -math.cos(self.ang) * self.radius))
            ang += 2 * math.pi / ASTEROID_GANULARITY
        # Draw polygon connecting vertices
        pg.draw.polygon(self.image, BLACK, self.vertices)
        # White outline
        for v in range(len(self.vertices)):
            if v == len(self.vertices) - 1:
                next_v = self.vertices[0]
            else:
                next_v = self.vertices[v + 1]   
            this_v = self.vertices[v]
            pg.draw.line(self.image, WHITE, this_v, next_v, 2)
   
    def update(self):
        self.pos.x += self.speed * math.cos(self.dir) * self.game.dt
        self.pos.y += self.speed * math.sin(self.dir) * self.game.dt
        self.rect.center = self.pos
        # Screen wrapping
        if self.pos.x - self.size > WIDTH:
            self.pos.x = 0 - self.size
        if self.pos.x + self.size < 0:
            self.pos.x = WIDTH + self.size
        if self.pos.y - self.size > HEIGHT:
            self.pos.y = 0 - self.size
        if self.pos.y + self.size < 0:
            self.pos.y = HEIGHT + self.size
        self.mask = pg.mask.from_surface(self.image)
