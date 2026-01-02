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


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        super().__init__()
        self.image = pygame.image.load("brick.png")
        
        self.rect = self.image.get_rect()
        if pos == "top":
            self.image = pygame.transform.flip(self.image, False, True) 
            self.rect.bottomleft = [x, y-pipegap//2]
        if pos == "bottom":
            self.rect.topleft = [x, y+pipegap//2]
    def update(self):
        self.rect.x -= scrollspeed
        if self.rect.right < 0:
                self.kill()

pipegroup = pygame.sprite.Group()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.birds = []
        for i in range(3):
            self.birds.append(pygame.transform.scale(pygame.image.load("mariohatwings.png"), (50, 50)))
        self.index = 0
            #(f"bird{1+1}.png")
        self.image = self.birds[0]
        self.rect = self.image.get_rect()
        # self.x = W//4
        # self.y = H//2
        self.rect.center = 100, H//2
        self.gravity = 0
        self.counter = 0

    def update(self):

        if fly and gamestage == "play":
            self.gravity += 1
            if self.gravity > 8:
                self.gravity = 8
            #if pyautogui.mouseDown() == True: - tried something but it crashed the computer for some reason

            if pygame.mouse.get_pressed()[0] == 1:
                self.gravity = -10
            if self.rect.bottom < H*(3/4):
                self.rect.y += self.gravity
                #print(self.rect.y)
            else:
                gameover = True
                flying = False
            self.index+=1
            if self.index > 2:
                self.index=0
            self.image = self.birds[self.index]
group = pygame.sprite.Group()
bird = Bird()
group.add(bird)
while True:
    sky.blit(bg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if gamestage == "start":
        title_text = font1.render("Mario Bird", True, (255, 255, 255))
        start_text = font2.render("Click to Start", True, (255, 255, 255))
        sky.blit(title_text, (W//2 - title_text.get_width()//2, H//3))
        sky.blit(start_text, (W//2 - start_text.get_width()//2, H//2))
        
        if pygame.mouse.get_pressed()[0]:
            gamestage = "play"
            fly = False
            gameover = False
            score = 0
            groundx = 0
            pipegroup.empty()
            bird.rect.center = (100, H//2)
            bird.gravity = 0
            lastpipe = pygame.time.get_ticks() - pipefrequency
    
    elif gamestage == "play":
        group.draw(sky)
        pipegroup.draw(sky)
        sky.blit(ground, (groundx, H - H//4))
        #score = score // 15
        score_text = font3.render(f"Score: {s}", True, (255, 255, 255))
        sky.blit(score_text, (10, 10))
        
        if pygame.sprite.groupcollide(group, pipegroup, False, False) or bird.rect.bottom >= H - H//4:
            gameover = True
            gamestage = "finish"

        if len(pipegroup) > 0:
            if group.sprites()[0].rect.left > pipegroup.sprites()[0].rect.right:
                score += 1
                s = score // 15
                print(score, s)
                # score = score // 15
                
        

        if fly and not gameover:
            groundx -= scrollspeed
            if groundx < -W//2:
                groundx = 0
            
            bird.update()
            
            timenow = pygame.time.get_ticks()
            if timenow - lastpipe > pipefrequency:
                pipeheight = random.randint(-100, 100)
                bottompipe = Pipe(W, H//2 + pipeheight, "bottom")
                toppipe = Pipe(W, H//2 + pipeheight, "top")
                pipegroup.add(bottompipe)
                pipegroup.add(toppipe)
                lastpipe = timenow
            pipegroup.update()

        if not gameover and not fly and pygame.mouse.get_pressed()[0]:
            fly = True
    
    elif gamestage == "finish":
        
        gameover_text = font1.render("Game Over", True, (255, 0, 0))
        final_score_text = font2.render(f"Final Score: {s}", True, (255, 255, 255))
        restart_text = font2.render("Click to Restart", True, (255, 255, 255))
        sky.blit(gameover_text, (W//2 - gameover_text.get_width()//2, H//3))
        sky.blit(final_score_text, (W//2 - final_score_text.get_width()//2, H//2))
        sky.blit(restart_text, (W//2 - restart_text.get_width()//2, H//2 + 50))
        
        if pygame.mouse.get_pressed()[0]:
            gamestage = "start"
    
    pygame.display.update()
