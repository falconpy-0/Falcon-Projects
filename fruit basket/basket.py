import pygame, sys
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fruit Basket")
icon = pygame.image.load("fruits-and-vegetables.png")
pygame.display.set_icon(icon)

# Load assets
background = pygame.image.load("background.jpg")
player_img = pygame.image.load("bucket.png")
fruit_img = pygame.image.load("strawberry.png")
heart_img = pygame.image.load("heart.png")

# Load sounds
bg_music = mixer.Sound("bgmusic.mp3")
catch_sound = mixer.Sound("catch.mp3")
life_sound = mixer.Sound("loselife.mp3")
gameover_sound = mixer.Sound("gameover.mp3")
bg_music.set_volume(0.5)

# Fonts
score_font = pygame.font.Font("freesansbold.ttf", 32)
gameover_font = pygame.font.Font("freesansbold.ttf", 64)


def run_game():
    # Start music
    bg_music.play(-1)

    # Game variables
    player_x = 370
    player_y = 450
    playerX_change = 0

    fruit_x = random.randint(0, 736)
    fruit_y = random.randint(50, 150)

    score = 0
    hearts = [(10, 10), (50, 10), (90, 10)]

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

        player_x += playerX_change
        player_x = max(0, min(player_x, 736))  # Boundary check

        # Fruit falling
        fruit_y += 4

        # Collision detection
        distance = math.sqrt((player_x - fruit_x)**2 + (player_y - fruit_y)**2)
        if distance < 27:
            catch_sound.play()
            score += 1
            fruit_x = random.randint(0, 736)
            fruit_y = 0

        elif fruit_y > 600:
            if hearts:
                life_sound.play()
                hearts.pop()
                fruit_x = random.randint(0, 736)
                fruit_y = 0
            if not hearts:
                gameover_sound.play()
                show_game_over(score)
                return  # Exit run_game

        # Draw player, fruit, score, hearts
        screen.blit(player_img, (player_x, player_y))
        screen.blit(fruit_img, (fruit_x, fruit_y))

        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 50))

        for pos in hearts:
            screen.blit(heart_img, pos)

        pygame.display.update()
        clock.tick(60)


def show_game_over(score):
    screen.fill((0, 0, 0))
    game_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
    score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = score_font.render("Press ENTER to Restart or ESC to Quit", True, (255, 255, 255))

    screen.blit(game_text, ((800 - game_text.get_width()) // 2, 200))
    screen.blit(score_text, ((800 - score_text.get_width()) // 2, 300))
    screen.blit(restart_text, ((800 - restart_text.get_width()) // 2, 380))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# MAIN LOOP
while True:
    run_game()
