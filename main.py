import pygame as pg
import random
from settings import *
from sprites import *
vec = pg.math.Vector2

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        print(pg.font.get_fonts())
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.player = Player(self)
        self.score = 0

        while len(self.asteroids) < DIFFICULTY:
            self.xrange = list(range(-ASTEROID_MAX_RADIUS,0)) + list(range(WIDTH, ASTEROID_MAX_RADIUS))
            self.yrange = list(range(-ASTEROID_MAX_RADIUS,0)) + list(range(HEIGHT, ASTEROID_MAX_RADIUS))
            self.asteroid = Asteroid(self, vec(random.choice(self.xrange), random.choice(self.yrange)), 'large')
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # Check collision between player and asteroid
        rect_collide = pg.sprite.spritecollide(self.player, self.asteroids, False)
        if rect_collide:
            mask_collide = pg.sprite.spritecollide(self.player, self.asteroids, False, pg.sprite.collide_mask)
            if mask_collide:
                self.playing = False
        # Check collision between bullet and asteroid
        rect_hit = pg.sprite.groupcollide(self.bullets, self.asteroids, False, False)
        if rect_hit:
            mask_hit = pg.sprite.groupcollide(self.asteroids, self.bullets, True, True, pg.sprite.collide_mask)
            for hit in mask_hit:
                if mask_hit and hit.asteroid_type == 'large':
                    self.asteroid = Asteroid(self, vec(hit.rect.centerx, hit.rect.centery), 'medium')
                    self.asteroid = Asteroid(self, vec(hit.rect.centerx, hit.rect.centery), 'medium')
                    self.score += 20
                if mask_hit and hit.asteroid_type == 'medium':
                    self.asteroid = Asteroid(self, vec(hit.rect.centerx, hit.rect.centery), 'small')
                    self.asteroid = Asteroid(self, vec(hit.rect.centerx, hit.rect.centery), 'small')
                    self.score += 50
                elif mask_hit and hit.asteroid_type == 'small':
                    self.xrange = list(range(-ASTEROID_MAX_RADIUS,0)) + list(range(WIDTH, ASTEROID_MAX_RADIUS))
                    self.yrange = list(range(-ASTEROID_MAX_RADIUS,0)) + list(range(HEIGHT, ASTEROID_MAX_RADIUS))
                    self.asteroid = Asteroid(self, vec(random.choice(self.xrange), random.choice(self.yrange)), 'large')
                    self.score += 100
    
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text('Score: ' + str(self.score), 22, WHITE, WIDTH * 0.05, HEIGHT * 0.05)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
while g.running:
    g.new()

pg.quit()
