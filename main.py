import pygame
import os

pygame.font.init()
pygame.mixer.init()

# creating a user event

YELLOW_HIT, RED_HIT = pygame.USEREVENT + 1, pygame.USEREVENT + 2

# RGB Colors
WHITE, BLACK, RED, YELLOW = (
    255, 255, 255), (1, 1, 1), (255, 0, 0), (255, 255, 0)
FPS = 60
VEL = 5

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_WIDTH, BULLET_HEIGHT,  BULLET_VEL, MAX_BULLETS = 10, 5, 10, 3
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3"))

WIDTH, HEIGHT = 900, 500  # Width and height of the game window
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH // 2 - BORDER_WIDTH // 2, 0, BORDER_WIDTH, HEIGHT)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# loading the assests

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def handle_yellow_movement(keys_pressed, yellow):
    if(keys_pressed[pygame.K_a] and yellow.x - VEL > 0):
        yellow.x -= VEL
    if(keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x):
        yellow.x += VEL
    if(keys_pressed[pygame.K_w] and yellow.y - VEL > 0):
        yellow.y -= VEL
    if(keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT):
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if(keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width):
        red.x -= VEL
    if(keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH):
        red.x += VEL
    if(keys_pressed[pygame.K_UP] and red.y - VEL > 0):
        red.y -= VEL
    if(keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT):
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() //
             2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()

    pygame.time.delay(5000)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    yellow_health_text = HEALTH_FONT.render(
        "Health: "+str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def main():
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(800, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y +
                                         yellow.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if(event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if(event.type == RED_HIT):
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if(event.type == YELLOW_HIT):
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if(yellow_health <= 0):
            winner_text = "Red Wins!!!"

        if(red_health <= 0):
            winner_text = "Yellow Wins!!!"

        if(winner_text != ""):
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets,
                    red_bullets, yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
