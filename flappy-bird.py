import pygame
import os
import random

# INITIAL CONFIG

# CONSTANT VARIABLES | SCREEN SIZE 
WIDTH_SCREEN = 500
HEIGHT_SCREEN = 800

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
IMAGES_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

# TEXT ON THE SCREEN
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("arial", 50)

# OBJECTS 
# (we have 3 objects that are in constant mouvement: bird, floor, pipe)

class Bird():
    IMGS = IMAGES_BIRD
    
    # rotate animation
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    TIME_ANIMATION = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0 
        self.height = self.y
        self.time = 0
        self.bird_image_count = 0
        self.bird_image = self.IMGS[0]

    def jump(self): # the bird only moves on the y axis 
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calculate the displacement
        self.time += 1
        displacement = 1.5 * (pow(self.time,2)) + self.speed * self.time
        
        # restrain the displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # bird's angle (parable mouvement when falling)
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
            else:
                if self.angle > -90:
                    self.angle =- self.SPEED_ROTATION


    def draw_bird(self, screen):

        # define which bird image we gonna use
        self.bird_image_count += 1

        # create the bird's wing mouvement
        if self.bird_image_count < self.TIME_ANIMATION:
            self.bird_image = self.IMGS[0]
        elif self.bird_image_count < self.TIME_ANIMATION * 2:
            self.bird_image = self.IMGS[1]
        elif self.bird_image < self.TIME_ANIMATION * 3:
            self.bird_image = self.IMGS[2]
        elif self.bird_image < self.TIME_ANIMATION * 4:
            self.bird_image = self.IMGS[1]
        elif self.bird_image < self.TIME_ANIMATION * 4 + 1:
            self.bird_image = self.IMGS[0]
        self.bird_image_count = 0

        # if the bird is falling, it doesn't have a wing mouvement
        if self.angle <= -80:
            self.bird_image = self.IMGS[1]
            self.bird_image_count = self.TIME_ANIMATION*2

        # draw the bird image
        rotate_bird_image = pygame.transform.rotate(self.bird_image, self.angle)
        pos_center_img = self.bird_image.get_rect(topleft = (self.x, self.y)).center
        rectangle = rotate_bird_image.get_rect(center=pos_center_img)
        screen.blit(rotate_bird_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.bird_image)

class Pipe():

    # CONST VARIABLES
    DISTANCE = 200 #px
    SPEED = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_base = 0
        self.TOP_PIPE = pygame.transform.flip(IMAGE_PIPE, False, True)
        self.BASE_PIPE = IMAGE_PIPE
        self.passed = False
        self.height_def()

    def height_def(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.TOP_PIPE.get_height()
        self.pos_base = self.height + self.DISTANCE

    def pipe_mouvement(self):
        self.x -= self.SPEED

    def draw_pipe(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.pos_top))
        screen.blit(self.BASE_PIPE, (self.x, self.pos_base))

    def colide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

        # verifies if a colision ocurred
        base_colision = bird_mask.overlap(base_mask, distance_base)
        top_colision = bird_mask.overlap(top_mask, distance_top)

        if base_colision or top_colision:
            return True
        else: 
            return False

class Floor():

    # CONSTANT VARIABLES
    SPEED = 5
    WIDTH = IMAGE_FLOOR.get_width()
    IMAGE = IMAGE_FLOOR

    def __init__(self, y):
        self.y = y
        self.floor1 = 0
        self.floor2 = self.WIDTH

    def move_floor(self):
        self.floor1 -= self.SPEED
        self.floor1 -= self.SPEED

        if self.floor1 + self.WIDTH < 0:
            self.floor1 = self.floor1 + self.WIDTH
        if self.floor2 + self.WIDTH < 0:
            self.floor2 = self.floor2 + self.WIDTH
        
    def draw_base(self, screen):
        screen.blit(self.IMAGE, (self.floor1, self.y))
        screen.blit(self.IMAGE, (self.floor2, self.y))

def draw_screen(screen, birds, pipes, floor, score):
    screen.blit(IMAGE_BACKGROUND, (0, 0))
    
    for bird in birds:
        bird.draw_bird(screen)
    
    for pipe in pipes:
        pipe.draw_pipe(screen)

    text = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255)) # RGB | White
    screen.blit(text, (WIDTH_SCREEN - 10 - text.get_width(), 10))

    floor.draw_base(screen)

    # screen update
    pygame.display.update()

    # GAME

def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    score = 0
    frame_update = pygame.time.Clock()

    game_on = True
    while game_on:

        # frames per second 
        frame_update.tick(30)

        # user's interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()
                quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        # MOUVEMENT - ELEMENTS
        for bird in birds:
            bird.move()

        floor.move_floor()

        add_pipe = False 
        remove_pipe = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colide(bird):
                    birds.pop(i)
                    
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
        
            pipe.pipe_mouvement()

        if pipe.x + pipe.TOP_PIPE.get_width() < 0:
            remove_pipe.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for pipe in remove_pipe:
            pipes.remove(pipe)

        for i,bird in enumerate(birds):
            if (bird.y + bird.bird_image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, score)
        
if __name__ == "__main__":
    main()