import pygame
import sys
import random
import asyncio

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

player_image = pygame.image.load("player.png").convert_alpha()

player_image = pygame.transform.scale(
    player_image,
    (50, 50)
)

cupcake_image = pygame.image.load(
    "cupcake.png"
).convert_alpha()

cupcake_image = pygame.transform.scale(
    cupcake_image,
    (30, 30)
)

async def main():
    
    player_x = 50
    player_y = 300

    player_dy = 0
    gravity = 0.5
    jump_speed = -10
    on_ground = True

    platforms = [
        pygame.Rect(0, 350, 600, 50),
        pygame.Rect(100, 270, 150, 20),
        pygame.Rect(350, 220, 150, 20)
    ]


    cupcakes = [
        pygame.Rect(150, 230, 30, 30),
        pygame.Rect(400, 180, 30, 30),
        pygame.Rect(520, 310, 30, 30)
    ]

    font = pygame.font.SysFont(None, 36)

    score = 0

    # MAIN LOOP
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= 5

        if keys[pygame.K_RIGHT]:
            player_x += 5

        if keys[pygame.K_UP] and on_ground:
            player_dy = jump_speed
            on_ground = False

        player_dy += gravity
        player_y += player_dy

        if player_y >= 300:
            player_y = 300
            player_dy = 0
            on_ground = True

        player_rect = pygame.Rect(player_x, player_y, 50, 50)

        for platform in platforms:
            if player_rect.colliderect(platform) and player_dy > 0:
                player_y = platform.top - 50
                player_dy = 0
                on_ground = True

        screen.fill((30, 30, 30))

        for platform in platforms:
            pygame.draw.rect(screen, (100, 180, 100), platform)


        for cupcake in cupcakes:
            screen.blit(
                cupcake_image,
                (cupcake.x, cupcake.y)
            )

        if len(cupcakes) == 0:
            cupcakes = []
            for i in range(3):
                x = random.randint(20, 590)
                y = random.randint(150, 320)
                cupcakes.append(pygame.Rect(x, y, 30, 30))
            
        screen.blit(player_image, (player_x, player_y))

        for cupcake in cupcakes[:]:
                if player_rect.colliderect(cupcake):
                    cupcakes.remove(cupcake)
                    score += 1
        
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
