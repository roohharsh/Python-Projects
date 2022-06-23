#initial step
import pygame
pygame.init()    #initialise pygame

win = pygame.display.set_mode((500,480))   # width & height of window (0,0) is at top left corner

pygame.display.set_caption("first game")   # window name

# animation movements (two list names walkRight & walkLeft)
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')    # bg image
char = pygame.image.load('standing.png')      # when character is not moving

clock = pygame.time.Clock()

# to add instant sound
bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')


# to add background sound
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)    # continuously play

score = 0

# now this class can be used for multiple players
class player(object):
    def __init__(self, x, y, width, height):
        # character's property
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel = 5
        # jumping variables
        self.isJump = False
        self.jumpCount = 10
        # Character animations
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True    # initially standing
        self.hitbox = (self.x+17, self.y+11, 29, 52)    # hitbox used for collision condition in pygame

    def draw(self, win):
        # redraw character as per its movement
        if self.walkCount + 1 >= 27:  # each sprite for three frames
            self.walkCount = 0

        # if character is not standing then move otherwise look into specific direction
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))  # integral division
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))  # integral division
                self.walkCount += 1
        else:
            # win.blit(char, (self.x, self.y)) # standing sprite
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))   # look in right
            else:
                win.blit(walkLeft[0], (self.x, self.y))  # look in left

        # hitbox for character
        self.hitbox = (self.x+17, self.y+11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)    # draw red color rectangular box

    # when character collides with enemy
    def hit(self):
        self.isJump = False     # fixing a bug
        self.jumpCount = 10
        self.x = 60     # reset to left
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render("-5", 1, (255, 0, 0))    # show that we lost 5 score
        win.blit(text, (250 - (text.get_width()/2), 200))     # in center of screen
        pygame.display.update()
        i=0
        while i < 300:
            pygame.time.delay(10)      # delay for showing text
            i += 1
            for event in pygame.event.get():   # if quit the game instead of wait for delay
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel = 8*facing      # left or right

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# enemies part
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        # hitbox for enemy
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        # health bar
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()      # first move character & then draw

        if self.visible:     # when character dies it will no more show on screen
            if self.walkCount + 1 >= 33:   # as 11 pics this time
                self.walkCount = 0

            if self.vel > 0:     # moving right
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            # health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # as health decrease health bar width also decrease
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10-self.health)), 10))

            # draw red color rectangular box
            self.hitbox = (self.x + 17, self.y+2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1    # change direction
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    # display when enemy is hit
    def hit(self):
        if self.health > 0:
            self.health-=1
        else:
            self.visible = False    # character dies
        print('hit')


# function for redraw game window
def redrawGameWindow():
    win.blit(bg, (0, 0))    # use blit to add picture

    text = font.render('Score: ' + str(score), 1, (0,0,0))    # blit text on screen
    win.blit(text, (350, 10))

    # draw a rectangle containing window color in rgb & set rectangle height width
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))

    man.draw(win)    # draw character on its movement
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()    # refresh the display so character shows in window


# main loop

font = pygame.font.SysFont('comicsans', 30, True)    # first true for bold & 2nd for italic
man = player(200, 410, 64, 64)    # man dimensions & position
goblin = enemy(100, 410, 64, 64, 450)    # enemies on screen
shootLoop = 0
bullets = []      # bullets list

run = True
while run:
    # pygame.time.delay(100)
    clock.tick(27)    # set FPS to 27

    # when enemy dies then there is no collision
    if goblin.visible == True:
        # if character & enemy collide then score decrease
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # as red cross clicked
            run = False


    for bullet in bullets:
        # bullet goes inside enemies hitbox
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()     # sound of hitting the enemy
                goblin.hit()
                if goblin.visible == True:
                    score += 1
                bullets.pop(bullets.index(bullet))   # move bullet from list if hit the enemy

    # bullets projectile
        if bullet.x < 500 and bullet.x > 0:    # allowed to shoot
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))    # remove bullet by finding its index in list

    # keys added to game & now character can move
    keys = pygame.key.get_pressed()

    # bullets
    if keys[pygame.K_SPACE] and shootLoop == 0:

        # bullet sound added
        bulletSound.play()

        if man.left:
            facing = -1    # bullet moving left
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0, 0, 0), facing))   # radius as 6

        shootLoop = 1

    # character
    if keys[pygame.K_LEFT] and man.x > man.vel:     # left boundary added
        man.x -= man.vel
        # character moves in left direction
        man.left = True
        man.right = False
        man.standing = False   # still walking
    elif keys[pygame.K_RIGHT] and man.x < 500-man.width-man.vel:   # right boundary added
        man.x += man.vel
        # character moves in right direction
        man.right = True
        man.left = False
        man.standing = False
    else:    # character is stationary
        man.standing = True
        man.walkCount = 0

    # jumping part (only way to move in vertical direction)
    if not(man.isJump):    # jump in vertical direction
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg    # jump in vertical direction
            man.jumpCount -= 1         # jump velocity decrease
        else:   # back to initial condition
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()     # call redraw function

pygame.quit()