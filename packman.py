import pygame
import os
import random



pygame.font.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")



# Load images
ENEMY1 = pygame.image.load(os.path.join("assets", "enemy1.png"))
ENEMY2 = pygame.image.load(os.path.join("assets", "enemy2.png"))
ENEMY3 = pygame.image.load(os.path.join("assets", "enemy3.png"))

FOOD1 = pygame.image.load(os.path.join("assets", "food1.png"))
FOOD2 = pygame.image.load(os.path.join("assets", "food2.png"))
FOOD3 = pygame.image.load(os.path.join("assets", "food3.png"))

PLAYER = pygame.image.load(os.path.join("assets", "player.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))




class Things:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.things_img = None


    def draw(self, window):
        window.blit(self.things_img, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, 70, 70)


    def get_width(self):
        return self.things_img.get_width()

    def get_height(self):
        return self.things_img.get_height()



class Player(Things):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.things_img = PLAYER
        self.mask = pygame.mask.from_surface(self.things_img)




class Enemy(Things):
    NUMBER_MAP = {
                "1": (ENEMY1),
                "2": (ENEMY2),
                "3": (ENEMY3)
    }
    def __init__(self, x, y, number):
        super().__init__(x, y)
        self.things_img = self.NUMBER_MAP[number]
        self.mask = pygame.mask.from_surface(self.things_img)
        self.hitbox = pygame.Rect(self.x, self.y, 70, 70)

    def move(self, vel):
        self.x -= vel
        if self.x <= 0:
            self.x = WIDTH
            self.y = random.randrange(0, HEIGHT - 100)


class Food(Things):
    NUMBER_MAP = {
                "one": (FOOD1),
                "two": (FOOD2),
                "three": (FOOD3)
    }
    def __init__(self, x, y, number):
        super().__init__(x, y)
        self.things_img = self.NUMBER_MAP[number]
        self.mask = pygame.mask.from_surface(self.things_img)
        self.hitbox = pygame.Rect(self.x, self.y, 70, 70)

    def move(self, vel):
        self.x -= vel
        if self.x <= 0:
            self.x = WIDTH
            self.y = random.randrange(0, HEIGHT - 100)


def main():
    run = True
    FPS = 60
    score = 0
    lives = 3
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)
    player_val = 5

    enemies = []
    fruits = []
    wave_length = 1
    food_val = 1
    enemy_val = 1



    player = Player(5, 400)



    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))
        #text
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 0, 0))
        score_label = main_font.render(f'Score: {score}', 1, (255,0,0))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (WIDTH - lives_label.get_width() - 30, 20))

        for enemy in enemies:
            enemy.draw(WIN)

        for food in fruits:
            food.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Game Over!", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200))


        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue



        if len(enemies) == 0:
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(500, 700), random.randrange(0, HEIGHT-100), random.choice(["1","2","3"]))
                enemies.append(enemy)


        if len(fruits) == 0:
            wave_length += 1
            for i in range(wave_length):
                food = Food(random.randrange(500, 700), random.randrange(100, HEIGHT-100), random.choice(["one","two","three"]))
                fruits.append(food)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_val > 0: #up
            player.y -= player_val
        if keys[pygame.K_DOWN] and player.y + player_val +70 < HEIGHT: #down
            player.y += player_val

        for enemy in enemies[:]:
            enemy.move(enemy_val)
            if player.hitbox.colliderect(enemy.hitbox):
                lives -=1
                enemies.remove(enemy)

        for food in fruits[:]:
            food.move(food_val)
            if player.hitbox.colliderect(food.hitbox):
                score += 1
                fruits.remove(food)



main()