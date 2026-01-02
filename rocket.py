import pgzrun, pyautogui, random
WIDTH, HEIGHT = pyautogui.size()
enemies = []
bullets = []
score = 0
lives = 3
galaga = Actor("gun", (WIDTH -100, HEIGHT // 2))
direction = 2
direction2 = 15
gamestage = "start"
enemybullets = []

def draw():
    global gamestage
    screen.clear()
    if gamestage == "start":
        screen.blit("battlefield", (0, 0))
        screen.draw.text("Gun Shooter", center=(WIDTH // 2, HEIGHT // 2 - 100), color="yellow", fontsize=100)
        screen.draw.text("Click to start the game", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=50)
    elif gamestage == "play":
        screen.blit("battlefield", (0, 0))
        galaga.draw()
        for i in enemies:
            i.draw()
        for i in bullets:
            i.draw()
        for i in enemybullets:
            i.draw()
       
    screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=40)
    screen.draw.text(f"Lives: {lives}", (WIDTH - 150, 10), color="white", fontsize=40)
    if lives <= 0:
        print(lives)
        gamestage = "Game Over"
        screen.clear()
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=100)
        screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 100), color="white", fontsize=60)
        screen.draw.text("Click to restart", center=(WIDTH // 2, HEIGHT // 2 + 200), color="white", fontsize=50)
        
def update():
    global direction, score, lives, gamestage, enemies, bullets, enemybullets
    # print(len(enemybullets))
    galaga.y += direction
    if galaga.y < 0 or galaga.y > HEIGHT:
        direction *= -1
    for i in enemies:
        i.x += 5
        if i.x > WIDTH:
            enemies.remove(i)
        for bullet in bullets:
            bullet.x -= 10
            if bullet.x < 0:
                bullets.remove(bullet)
            if bullet.colliderect(i):
                enemies.remove(i)
                bullets.remove(bullet)
                score += 1
    
        if galaga.colliderect(i):
            enemies.remove(i)
            lives-=1
        # if gamestage == "Game Over":
        #     enemies = []
        #     bullets = []
            # if on_mouse_down:
            #     gamestage = "restart"
            #     score = 0
            #     lives = 3
            #     screen.draw.text("Click to restart", center=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=50)
                # if gamestage == "restart":
                #         gamestage = "start"
                    
        
        

        #for bullet in bullets:
            # bullet.x -= 10
            # if bullet.x < 0:
            #     bullets.remove(bullet)
            # if bullet.colliderect(i):
            #     if i in enemybullets:
            #         enemybullets.remove(i)
            #     if bullet in bullets:
            #         bullets.remove(bullet)
            #     score += 1
    for i in enemies:
        if random.randint(0, 100) < 3:
            enemybullet = Actor("bullet2 (2)", (i.x, i.y + 8))
            enemybullets.append(enemybullet)
    for eb in enemybullets:
        eb.x += 10
        if eb.x > WIDTH:
            enemybullets.remove(eb)
        for bullet in bullets:
            if eb.colliderect(bullet):
                enemybullets.remove(eb)
                bullets.remove(bullet)
                score += 1
        if eb.colliderect(galaga):
            enemybullets.remove(eb)
            lives -= 1
                
def on_key_down(key):
    if key == keys.UP:
        galaga.y -= 10
    elif key == keys.DOWN:
        galaga.y += 10

def on_mouse_down(pos):
    global gamestage, bullets, enemies, score, lives
    bullet = Actor("bullet2 (2)", (galaga.x, galaga.y + 8))
    bullets.append(bullet)
    if gamestage == "start":
        gamestage = "play"
        return
    elif gamestage == "Game Over":
        gamestage = "restart"
        enemies = []
        bullets = []
        score = 0
        lives = 3
        return
def actors():
    if gamestage == "play":
        villain = Actor("bug2", (0,random.randint(0, WIDTH)))
        enemies.append(villain)

def create_enemy_bullet():
    for i in enemies:
        enemybullet = Actor("bullet2", (i.x, i.y + 8))
        enemybullets.append(enemybullet)
              
    
clock.schedule_interval(actors, 1.0)


pgzrun.go()