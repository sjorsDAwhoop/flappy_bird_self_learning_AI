import pygame
import neat
import time
import os
import random
pygame.font.init()


WIN_WIDTH = 600
WIN_HEIGHT = 800

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird3.png")))]
pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "base.png")))
bg_image = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bg.png")))

stat_font = pygame.font.SysFont("Calibri", 50)

class Bird:
    images = bird_images
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.images[0]
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel
                
    def draw(self,win):
        self.img_count += 1

        if self.img_count < self.animation_time:
            self.img = self.images[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.images[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.images[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.images[1]
        elif self.img_count < self.animation_time*4 + 1:
            self.img = self.images[0]
            self.img_count = 0
            
        if self.tilt <= -80:
            self.img = self.images[1]
            self.img_count = self.animation_time*2
            
        # rotates the birds
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    gap = 200
    vel = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_image, False, True)
        self.pipe_bottom = pipe_image

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
         self.x -= self.vel

    def draw(self,win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bot_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bot_point:
            return True
        
        return False
        

class Base:
    vel = 5
    width = base_image.get_width()
    img = base_image

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2+ self.width

        if self.x2+ self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img,(self.x1, self.y))
        win.blit(self.img,(self.x2, self.y))
    
    
      
def draw_window(win, bird, pipes, base, score):
    win.blit(bg_image,(0,0))
    
    for pipe in pipes:
        pipe.draw(win)

    text = stat_font.render("score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()

        add_pipe = False
        
        #remove pipes
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
            pipe.move()
                
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass
            
            
        base.move()
               
        draw_window(win, bird, pipes, base, score)
        
    pygame.quit()
    quit()

main()

    
    


