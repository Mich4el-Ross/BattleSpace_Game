import pygame
import os
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Space Battle")    # Setting the window caption

WIDTH, HEIGHT = 900, 500;                       # Width and Height of my display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Setting the game display

WHITE = (255, 255, 255)     # Setting the display color (RGB)
GRAY = (80, 80, 80)         # Setting the border color (RGB)
RED = (255, 0, 0)           # Setting the red bullet color (RGB)
YELLOW = (255, 255, 0)      # Setting the yellow bullet color (RGB)

BORDER = pygame.Rect((WIDTH // 2 - 5), 0, 10, HEIGHT)  # X, Y, WIDTH, HEIGHT

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hitSound.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/fireSound.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4
SPACESHIP_WDT, SPACESHIP_HGT = 75, 60

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WDT, SPACESHIP_HGT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WDT, SPACESHIP_HGT)), 270)

SPACE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(WIN, GRAY, BORDER)

    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH  - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):

    # Yellow spaceship is placed on the left-handle side of the screen
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:    # LEFT KEY
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:    # RIGHT KEY
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL  > 0:    # UP KEY
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:    # DOWN KEY
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):

    # Red spaceship is placed on the right-handle side of the screen
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 25: # LEFT KEY
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 10 < WIDTH: # RIGHT KEY
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:   # UP KEY
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # DOWN KEY
        red.y += VEL        


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text, color):
    winner_msg = WINNER_FONT.render(text, 1 , color)
    WIN.blit(winner_msg, (WIDTH//2 - winner_msg.get_width()//2, HEIGHT//2 - winner_msg.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WDT, SPACESHIP_HGT)       # Rectangle that catch the red_spaceship position
    yellow = pygame.Rect(100, 300, SPACESHIP_WDT, SPACESHIP_HGT)    # Rectangle that catch the yellow_spaceship position
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins!'
            color = YELLOW
        if yellow_health <= 0:
            winner_text = 'Red Wins!'
            color = RED

        if winner_text != '':
            draw_winner(winner_text, color)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)    # YELLOW SPACESHIP MOVEMENTS 
        red_handle_movement(keys_pressed, red)          # RED SPACESHIP MOVEMENTS
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

# The program is just executed if this file be run
if __name__ == "__main__":
    main()