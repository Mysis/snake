__author__ = 'Misys'
import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIMENSIONS = (768, 512)

class Game():

    def __init__(self):

        self.screen = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption("snake")
        self.clock = pygame.time.Clock()

        self.allSpritesGroup = pygame.sprite.Group()
        self.fruitGroup = pygame.sprite.GroupSingle()

        self.snake = SnakeHead(128, 128, RIGHT, 5, self.allSpritesGroup)
        self.allSpritesGroup.add(self.snake)
        fruit = Fruit(self.allSpritesGroup)
        self.fruitGroup.add(fruit)

        self.score = 0

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not self.snake.direction == DOWN:
                self.snake.direction = UP
            elif keys[pygame.K_RIGHT] and not self.snake.direction == LEFT:
                self.snake.direction = RIGHT
            elif keys[pygame.K_DOWN] and not self.snake.direction == UP:
                self.snake.direction = DOWN
            elif keys[pygame.K_LEFT] and not self.snake.direction == RIGHT:
                self.snake.direction = LEFT

            self.allSpritesGroup.update()

            if pygame.sprite.spritecollideany(self.snake, self.fruitGroup):
                self.score += 100
                self.snake.length += 5
                for segment in self.snake.segmentsGroup:
                    segment.ttl += 5
                self.fruitGroup.sprite.kill()
                fruit = Fruit(self.allSpritesGroup)
                self.fruitGroup.add(fruit)

            self.screen.fill(BLACK)
            self.allSpritesGroup.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(20)

class SnakeHead(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, length, allSpritesGroup):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((16, 16))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = direction
        self.length = length

        self.allSpritesGroup = allSpritesGroup
        self.segmentsGroup = pygame.sprite.Group()

    def update(self):

        segment = SnakeSegment(self.rect.x, self.rect.y, self.length)
        self.allSpritesGroup.add(segment)
        self.segmentsGroup.add(segment)

        if self.direction == UP:
            self.rect.y -= 16
        if self.direction == RIGHT:
            self.rect.x += 16
        if self.direction == DOWN:
            self.rect.y += 16
        if self.direction == LEFT:
            self.rect.x -= 16

        if self.rect.x < 0:
            self.rect.x = DIMENSIONS[0] - 16
        elif self.rect.x > DIMENSIONS[0] - 16:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = DIMENSIONS[1] - 16
        elif self.rect.y > DIMENSIONS[1] - 16:
            self.rect.y = 0

        if pygame.sprite.spritecollideany(self, self.segmentsGroup):
            input("YOU LOSE!")
            quit()

class SnakeSegment(pygame.sprite.Sprite):

    def __init__(self, x, y, ttl):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.ttl = ttl

    def update(self):

        self.ttl -= 1
        if not self.ttl > 0:
            self.kill()

class Fruit(pygame.sprite.Sprite):

    def __init__(self, allSpritesGroup):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((16, 16))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, DIMENSIONS[0]/16 - 1) * 16
        self.rect.y = random.randint(0, DIMENSIONS[1]/16 - 1) * 16

        while pygame.sprite.spritecollideany(self, allSpritesGroup):
            self.rect.x = random.randint(0, DIMENSIONS[0]/16 - 1) * 16
            self.rect.y = random.randint(0, DIMENSIONS[1]/16 - 1) * 16

        allSpritesGroup.add(self)

game = Game()