import pygame
import sys
import random
from hangman import get_word_from_file, check_high_score, play_game

def create_buttons():
    star_x = 50
    star_y = 450
    spacing = 55

    buttons = []
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i, letter in enumerate(alphabets):
        x = star_x + (i % 13) * spacing
        y = star_y + (i // 13) * spacing
        button_rect = pygame.Rect(x, y, 50, 50)
        buttons.append({"letter": letter, "rect": button_rect, "clicked": False})

    return buttons

def create_answers():
    display_text =" ".join(display)
    text_img = title_font.render(display_text, True, (0, 0, 0))
    screen.blit(text_img, (300, 300))


pygame.init()
title_font = pygame.font.SysFont("arial", 60)
screen = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption("My Hangman Game")

words_list = get_word_from_file("words.txt") # 단어장 파일 이름
secret_word = random.choice(words_list).upper()
display = ['_'] * len(secret_word)
penalty = 0
attempts = 0

running = True
buttons = create_buttons()
button_font = pygame.font.SysFont("arial", 40)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for btn in buttons:
                if btn["rect"].collidepoint(mouse_pos):
                    if not btn["clicked"]:
                        btn["clicked"] = True
                        
                        clicked_letter = btn["letter"] 
                        
                        display, penalty, attempts = play_game(
                            secret_word, display, penalty, attempts, clicked_letter
                        )

    screen.fill((255, 255, 255))

    create_answers()
    
    for btn in buttons:
        if btn["clicked"]:
            pygame.draw.rect(screen, (200, 200, 200), btn["rect"])
        else:
            pygame.draw.rect(screen, (0, 0, 0), btn["rect"], 2)
            letter_img = button_font.render(btn["letter"], True, (0, 0, 0))
            screen.blit(letter_img, (btn["rect"].x + 12 , btn["rect"].y))
    pygame.display.flip()

pygame.quit()
sys.exit()