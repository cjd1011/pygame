# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 19:56:51 2023

@author: cjdiaz
"""

import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Salvemos a Colombia del Comunismo")

# Set up the player character
player_size = 50
player_x = (window_width - player_size) // 2
player_y = window_height - player_size

# Set up the enemies
enemy_size = 50
num_enemies = 8
enemies = []
enemy_speed = 1  # Initial enemy speed
for _ in range(num_enemies):
    enemy_x = random.randint(0, window_width - enemy_size)
    enemy_y = random.randint(-window_height, 0)
    enemies.append((enemy_x, enemy_y, enemy_speed))

flag_image = pygame.image.load("Colombian_flag.png").convert_alpha()
flag_image = pygame.transform.scale(flag_image, (player_size, player_size))

# Load the enemy image
enemy_image = pygame.image.load("petro_borracho.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

# Set up the game loop
clock = pygame.time.Clock()
running = True
game_over = False
score = 0
level = 1

# Set up the font for the score and level display
font = pygame.font.Font(None, 36)

# Display the start message
start_message = font.render("Salvemos a Colombia del Comunismo", True, (255, 255, 255))
start_message_rect = start_message.get_rect(center=(window_width // 2, window_height // 2))


while running:
    clock.tick(60)  # Set the desired frame rate (60 FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if not game_over:
                # Start the game when any key is pressed
                start_message = None
            else:
                # Reset the game when any key is pressed after game over
                game_over = False
                score = 0
                level = 1
                for i in range(num_enemies):
                    enemy_x = random.randint(0, window_width - enemy_size)
                    enemy_y = random.randint(-window_height, 0)
                    enemies[i] = (enemy_x, enemy_y, enemy_speed)

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player_x -= 5
        if keys[K_RIGHT]:
            player_x += 5
        if keys[K_UP]:
            player_y -= 5
        if keys[K_DOWN]:
            player_y += 5

        # Update the enemies' positions and speed
        for i in range(num_enemies):
            enemy_x, enemy_y, enemy_speed = enemies[i]
            enemy_y += enemy_speed
            if enemy_y >= window_height:
                enemy_x = random.randint(0, window_width - enemy_size)
                enemy_y = random.randint(-window_height, 0)
                score += 1  # Increase score when an enemy reaches the bottom
                enemy_speed += 0.5  # Increase enemy speed
            enemies[i] = (enemy_x, enemy_y, enemy_speed)

        # Check for collision with the player
        for enemy_x, enemy_y, _ in enemies:
            if (
                player_x < enemy_x + enemy_size
                and player_x + player_size > enemy_x
                and player_y < enemy_y + enemy_size
                and player_y + player_size > enemy_y
            ):
                game_over = True
                break

        # Clear the screen
        window.fill((0, 0, 0))

        # Draw the player character
        window.blit(flag_image, (player_x, player_y))

        # Draw the enemies
        for enemy_x, enemy_y, _ in enemies:
            window.blit(enemy_image, (enemy_x, enemy_y))

        # Draw the score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        # Draw the level
        level = (score // 10) + 1  # Calculate the level based on the score
        level_text = font.render("Level: " + str(level), True, (255, 255, 255))
        window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

        # Update the display
        pygame.display.update()

    else:
        # Display game over message
        game_over_text = font.render("A vivir Sabroso como Venezuela", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(game_over_text, text_rect)
        pygame.display.update()
        
    if start_message:
        # Display start message
        window.blit(start_message, start_message_rect)
        pygame.display.update()    

pygame.quit()
