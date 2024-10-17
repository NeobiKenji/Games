#Create your own shooter
from time import time as timer
from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
life = 3
goal = 15
score = 0
lost = 0
max_lost = 3
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('VICTORY!', True, (255, 255, 255))
lose = font1.render('DEFEAT!', True, (180,0,0))

font2 = font.SysFont('Arial', 36)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound =  mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80 , win_width-80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80),-40, 80,50,randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
clock = time.Clock()
finish = False
run = True
FPS = 120
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 6 and rel_time == False:
                    num_fire = num_fire +1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 6 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0,0))
        asteroids.update()
        ship.update()
        monsters.update()
        bullets.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire= 0
                rel_time = False

        collide = sprite.groupcollide(monsters, bullets, True, True)
        for c in collide:
            score = score +1
            monster = Enemy(img_enemy, randint (80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        text = font2.render('Score:' + str(score), 1, (255,255,255)) 
        window.blit(text, (10, 20))

        text_lose = font2.render('Missed:'+ str(lost), 1,  (255, 255, 255))
        if life ==3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color= (150,0,0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()

    time.delay(50)