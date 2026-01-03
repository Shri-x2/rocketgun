import pygame, pyautogui, random
pygame.init()

W, H = pyautogui.size()
sky = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mario Bird")

gamestage = "start"
font1 = pygame.font.SysFont("Retro Mario", 75)
font2 = pygame.font.SysFont("Super Mario", 35)
font3 = pygame.font.SysFont("Mario Luigi 2", 25)

fly = False
gameover = False

bg = pygame.transform.scale(pygame.image.load("mariobg.png"), (W, H))
ground = pygame.transform.scale(pygame.image.load("marioground2.png"), (W*1.5, H//4))

groundx = 0
scrollspeed = 5
pipefrequency = 2000
lastpipe = pygame.time.get_ticks() - pipefrequency
pipegap = 200

score = 0
s = 0
lives = 3  # ✅ add lives

# Small cooldown to avoid losing multiple lives in 1 frame
crash_cooldown_ms = 800
last_crash_time = -999999


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        super().__init__()
        self.image = pygame.image.load("brick.png")
        self.rect = self.image.get_rect()
        if pos == "top":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipegap // 2]
        if pos == "bottom":
            self.rect.topleft = [x, y + pipegap // 2]

    def update(self):
        self.rect.x -= scrollspeed
        if self.rect.right < 0:
            self.kill()


pipegroup = pygame.sprite.Group()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.birds = []
        for _ in range(3):
            self.birds.append(
                pygame.transform.scale(pygame.image.load("mariohatwings.png"), (50, 50))
            )
        self.index = 0
        self.image = self.birds[0]
        self.rect = self.image.get_rect()
        self.rect.center = (100, H // 2)
        self.gravity = 0

    def update(self, fly, gamestage):
        # ✅ Only update physics in play mode while flying
        if fly and gamestage == "play":
            self.gravity += 1
            if self.gravity > 8:
                self.gravity = 8

            if pygame.mouse.get_pressed()[0] == 1:
                self.gravity = -10

            self.rect.y += self.gravity

            # Animate
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.birds[self.index]


group = pygame.sprite.Group()
bird = Bird()
group.add(bird)


def respawn():
    """✅ reset round without ending the game"""
    global fly, groundx, lastpipe
    fly = False
    groundx = 0
    pipegroup.empty()
    bird.rect.center = (100, H // 2)
    bird.gravity = 0
    lastpipe = pygame.time.get_ticks() - pipefrequency


while True:
    sky.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if gamestage == "start":
        title_text = font1.render("Mario Bird", True, (255, 255, 255))
        start_text = font2.render("Click to Start", True, (255, 255, 255))
        sky.blit(title_text, (W // 2 - title_text.get_width() // 2, H // 3))
        sky.blit(start_text, (W // 2 - start_text.get_width() // 2, H // 2))

        if pygame.mouse.get_pressed()[0]:
            gamestage = "play"
            fly = False
            gameover = False
            score = 0
            s = 0
            lives = 3  # ✅ reset lives
            respawn()

    elif gamestage == "play":
        # Draw sprites + ground
        group.draw(sky)
        pipegroup.draw(sky)
        sky.blit(ground, (groundx, H - H // 4))

        # HUD
        score_text = font3.render(f"Score: {s}", True, (255, 255, 255))
        lives_text = font3.render(f"Lives: {lives}", True, (255, 255, 255))
        sky.blit(score_text, (10, 10))
        sky.blit(lives_text, (10, 40))

        # Start flying on first click
        if not gameover and not fly and pygame.mouse.get_pressed()[0]:
            fly = True

        # Update physics + scrolling only if flying and not gameover
        if fly and not gameover:
            groundx -= scrollspeed
            if groundx < -W // 2:
                groundx = 0

            bird.update(fly, gamestage)

            # Spawn pipes
            timenow = pygame.time.get_ticks()
            if timenow - lastpipe > pipefrequency:
                pipeheight = random.randint(-100, 100)
                bottompipe = Pipe(W, H // 2 + pipeheight, "bottom")
                toppipe = Pipe(W, H // 2 + pipeheight, "top")
                pipegroup.add(bottompipe)
                pipegroup.add(toppipe)
                lastpipe = timenow

            pipegroup.update()

            # Score logic (same as your approach)
            if len(pipegroup) > 0:
                if group.sprites()[0].rect.left > pipegroup.sprites()[0].rect.right:
                    score += 1
                    s = score // 15

        # ✅ Collision / ground check -> lose a life, don’t end immediately
        hit_pipe = pygame.sprite.groupcollide(group, pipegroup, False, False)
        hit_ground = bird.rect.bottom >= (H - H // 4)

        if (hit_pipe or hit_ground) and not gameover:
            now = pygame.time.get_ticks()
            if now - last_crash_time > crash_cooldown_ms:
                last_crash_time = now
                lives -= 1

                if lives <= 0:
                    gameover = True
                    gamestage = "finish"
                else:
                    respawn()

    elif gamestage == "finish":
        gameover_text = font1.render("Game Over", True, (255, 0, 0))
        final_score_text = font2.render(f"Final Score: {s}", True, (255, 255, 255))
        restart_text = font2.render("Click to Restart", True, (255, 255, 255))
        sky.blit(gameover_text, (W // 2 - gameover_text.get_width() // 2, H // 3))
        sky.blit(final_score_text, (W // 2 - final_score_text.get_width() // 2, H // 2))
        sky.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 50))

        if pygame.mouse.get_pressed()[0]:
            gamestage = "start"

    pygame.display.update()
