import pygame
import sys
import random
import time
import os

ICON_PATH = os.path.join(os.path.dirname(__file__), "Py-pong.png")
icon_surface = pygame.image.load(ICON_PATH)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Py-Pong")
pygame.display.set_icon(icon_surface)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_width, paddle_height = 10, 100
player1 = pygame.Rect(50, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)  # Jugador
player2 = pygame.Rect(WIDTH - 60, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)  # IA

ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
ball_speed_x = 5
ball_speed_y = 5

paddle_speed = 7
ia_speed = 4

clock = pygame.time.Clock()

ia_precision = 0.9
ia_decision_interval = 0.5
last_ia_decision_time = time.time()
target_y = ball.centery
score_player = 0
score_ai = 0
game_active = True

if game_active:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1.top > 0:
                player1.y -= paddle_speed
            if keys[pygame.K_s] and player1.bottom < HEIGHT:
                player1.y += paddle_speed

            current_time = time.time()
            if current_time - last_ia_decision_time > ia_decision_interval:
                last_ia_decision_time = current_time
                if random.random() < ia_precision:
                    target_y = ball.centery
                else:
                    target_y = random.randint(0, HEIGHT)

            if player2.centery < target_y and player2.bottom < HEIGHT:
                player2.y += ia_speed
            elif player2.centery > target_y and player2.top > 0:
                player2.y -= ia_speed

            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y *= -1
            if ball.colliderect(player1) or ball.colliderect(player2):
                ball_speed_x *= -1

            if ball.left <= 0:
                score_ai += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x *= -1
            if ball.right >= WIDTH:
                score_player += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x *= -1

            if score_player >= 5 or score_ai >= 5:
                game_active = False

        screen.fill(BLACK)

        if game_active:
            pygame.draw.rect(screen, WHITE, player1)
            pygame.draw.rect(screen, WHITE, player2)
            pygame.draw.ellipse(screen, WHITE, ball)
            pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            font = pygame.font.SysFont(None, 60)
            score_text = font.render(f"{score_player}   {score_ai}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        else:
            font = pygame.font.SysFont(None, 80)
            if score_player >= 5:
                end_text = font.render("YOU WON!", True, WHITE)
            else:
                end_text = font.render("GAME OVER", True, WHITE)
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
            if not game_active:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    score_player = 0
                    score_ai = 0
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    game_active = True
        pygame.display.flip()
        clock.tick(60)



