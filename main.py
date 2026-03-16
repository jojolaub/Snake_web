import pygame
import random
import asyncio

# 1. Konstanten
BREITE = 600
HEIGHT = 400
ROT = (255, 0, 0)
GRUEN = (0, 255, 0)
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)

async def main():
    # 2. Initialisierung
    pygame.init()
    screen = pygame.display.set_mode((BREITE, HEIGHT))
    pygame.display.set_caption("Snake Web Version")
    clock = pygame.time.Clock()
    
    # Sicherer Font für Webbrowser (None nutzt den Standard-Font)
    font = pygame.font.Font(None, 36)

    # Start-Zustand
    x, y = 300, 200
    x_change, y_change = 0, 0
    snake_length = 1
    liste = []
    
    # Futter-Position
    x_food = random.randrange(0, BREITE, 10)
    y_food = random.randrange(0, HEIGHT, 10)
    
    running = True

    # 3. Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Steuerung
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -20, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = 20, 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change, x_change = -20, 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change, x_change = 20, 0

        # Bewegung
        x += x_change
        y += y_change

        # Kollision mit dem Rand
        if x < 0 or y < 0 or x >= BREITE or y >= HEIGHT:
            running = False
        
        # Kopf-Logik
        kopf = [x, y]
        if (x_change != 0 or y_change != 0) and kopf in liste:
            running = False

        liste.append(kopf)
        if len(liste) > snake_length:
            del liste[0]

        # Futter essen
        if x == x_food and y == y_food:
            snake_length += 1
            x_food = random.randrange(0, BREITE, 20)
            y_food = random.randrange(0, HEIGHT, 20)

        # 4. Zeichnen
        screen.fill(SCHWARZ)
        
        # Score anzeigen
        score_bild = font.render(f"Punkte: {snake_length - 1}", True, WEISS)
        screen.blit(score_bild, [20, 20])

        # Schlange zeichnen
        for segment in liste:
            pygame.draw.rect(screen, GRUEN, [segment[0], segment[1], 20, 20])
        
        # Apfel zeichnen
        pygame.draw.rect(screen, ROT, [x_food, y_food, 20, 20])

        pygame.display.update()
        
        # 5. Browser-Magie (Wichtig!)
        await asyncio.sleep(0) 
        clock.tick(10) # 15 FPS für flüssiges Snake

    # 6. Game Over Screen
    screen.fill(SCHWARZ)
    game_over_text = font.render("GAME OVER!", True, ROT)
    screen.blit(game_over_text, [BREITE // 2 - 80, HEIGHT // 2 - 20])
    pygame.display.update()
    
    # 3 Sekunden warten vor dem Beenden (Web-kompatibel)
    await asyncio.sleep(3)
    print("Spiel beendet")

# Start-Befehl
if __name__ == "__main__":
    asyncio.run(main())