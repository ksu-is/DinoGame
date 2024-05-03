import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)

# Classes


class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/DinoDucking1.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/DinoDucking2.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 4.5
        self.ducking = False
        self.is_flipped = False
        self.on_fground = False

    def flip(self):
        self.is_flipped = not self.is_flipped
        if self.is_flipped:
            self.rect.y = 125
            self.on_fground = True
        else:
            self.rect.y = 500
            self.on_fground = False

    def jump(self):
        jump_sfx.play()
        if self.rect.centery >= 540:
            while self.rect.centery - self.velocity > 180:
                self.rect.centery -= 1
    
    def duck(self):
        self.ducking = True
        if self.on_fground:
            self.rect.centery = 115
        else:
            self.rect.centery = 560

    def unduck(self):
        self.ducking = False
        if self.on_fground:
            self.rect.centery =125
        else:
            self.rect.centery = 540

    def apply_gravity(self):
        if self.on_fground:
            if self.rect.centery <= 125:
                self.rect.centery +=self.gravity
        elif self.rect.centery <= 540:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            if self.on_fground:
                self.image = pygame.transform.flip(self.ducking_sprites[int(self.current_image)], False, True)
            else:
                self.image = self.ducking_sprites[int(self.current_image)]
        else:
            if self.on_fground:
                self.image = pygame.transform.flip(self.running_sprites[int(self.current_image)], False, True)
            else:
                self.image = self.running_sprites[int(self.current_image)]


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/cacti/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class FCactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/fcacti/fcactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([180, 520, 470, 210])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

# Variables


game_speed = 4
jump_count = 5
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 750

# Surfaces

ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1300, 25))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (350, 140))

fground = pygame.image.load("assets/flipedground.png")
fground = pygame.transform.scale(fground, (1300,25))
fground_x = 0
fground_rect = fground.get_rect(center=(640,400))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 540)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Functions


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()

fground_gravity = 0

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 350)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0
            elif event.key == pygame.K_f:
                dinosaur.flip()
                if dinosaur.on_fground:
                    dinosaur.apply_gravity()

    screen.fill("white")

    # Collisions
    if not dinosaur.on_fground:
        if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
            game_over = True
            death_sfx.play()
        if game_over:
            end_game()

    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 535)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(10, 13):
                new_obstacle = FCactus(1280, 130)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed
        fground_x -= game_speed

        fground_rect.y += fground_gravity

        screen.blit(ground, (ground_x, 550))
        screen.blit(ground, (ground_x + 1280, 550))

        screen.blit(fground, (fground_x, 125))
        screen.blit(fground, (fground_x + 1280, 125))

        if ground_x <= -1280:
            ground_x = 0
        if fground_x <= -1280:
            fground_x = 0

    clock.tick(120)
    pygame.display.update()