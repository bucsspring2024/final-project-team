import pygame
import pyautogui
import random
import os

pygame.init()

width, height = pyautogui.size()
width_2 = width//2
height_2 = height//2

screen = pygame.display.set_mode((width, height))

screen = pygame.display.set_mode((width, height))

run = [pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png"))]

jump = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))

duck = [pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png"))]

cactus_small = [pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png"))]

cactus_large = [pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png"))]

bird = [pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("assets/Bird", "Bird2.png"))]

cloud = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

background = pygame.image.load(os.path.join("assets/Other", "Ground.png"))


class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    jump_vel = 10

    def __init__(self):
        self.duck_img = duck
        self.run_img = run
        self.jump_img = jump

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.jump_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, user_input):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.jump_vel:
            self.dino_jump = False
            self.jump_vel = self.jump_vel

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = width + random.randint(500, 1000)
        self.y = random.randint(50, 200)
        self.image = cloud
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 40
    x_pos_bg = 0
    y_pos_bg = 400
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 80)
        screen.blit(text, textRect)

    def draw_background():
        global x_pos_bg, y_pos_bg
        image_width = background.get_width()
        screen.blit(background, (x_pos_bg, y_pos_bg))
        screen.blit(background, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(background, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    
    def save_score():
        with open("results.txt", "a") as file:
            file.write(f"Death Count: {death_count}, Score: {points}\n")
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(screen)
        player.update(user_input)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(cactus_small))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(cactus_large))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(3000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(screen)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count, run_images):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (width_2, height_2 + 50)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (width_2, height_2)
        screen.blit(text, textRect)
        
        screen.blit(run_images[0], (width_2 - 20, height_2 - 140))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0, run_images=run)