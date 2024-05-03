import pygame
import random

# Initialize Pygame
pygame.init()

# Set display dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set display and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Space Invaders")
clock = pygame.time.Clock()

# Load music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound('bulletShot.mp3')

# Load images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')
enemy_bullet_img = pygame.image.load('enemy_bullet.png')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-40, -30)
        self.speed = random.choice([-2, 2])
        self.shoot_delay = random.randint(500, 2000)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.rect.y += 40
            self.speed *= -1

        if self.rect.y > HEIGHT:
            self.rect.y = random.randrange(-200, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speed = random.choice([-2, 2])

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy Bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Score
score = 0
font = pygame.font.Font(None, 36)

def show_main_menu():
    title_font = pygame.font.Font(None, 64)
    press_space_font = pygame.font.Font(None, 36)
    
    main_menu = True
    while main_menu:
        screen.fill(BLACK)
        
        title_text = title_font.render("AI Space Invaders", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(title_text, title_rect)
        
        press_space_text = press_space_font.render("Press Space to Start", True, WHITE)
        press_space_rect = press_space_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(press_space_text, press_space_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_menu = False
        pygame.display.flip()
        clock.tick(FPS)

def show_game_over_screen(score):
    game_over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 36)
    
    game_over = True
    while game_over:
        screen.fill(BLACK)
        
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = score_font.render("Score: " + str(score), True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(score_text, score_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_over = False
        pygame.display.flip()
        clock.tick(FPS)

show_main_menu()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 10  # Increase score when an enemy is hit

    enemy_bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    if enemy_bullet_hits:
        show_game_over_screen(score)
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()