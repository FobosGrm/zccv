 from pygame import *
from random import randint
from time import time as timer

mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()

#fire_sound = mixer.Sound('fire.ogg')
#fire_sound.play()

font.init()
font1 = font.Font(None, 50)
font2 = font.Font(None, 30)
lose = font1.render("You Lose", True, (180, 0, 0))
win = font1.render("You Win", True, (180, 0, 0))

img_back = "galaxy.jpg" 
img_hero = "rocket.png"  
img_bullet = "bullet.png" 
img_enemy = "ufo.png"   
 
score = 0  
lost = 0
goal = 5  
max_lost = 300 
ray_fire = 10


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 50:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 10, self.rect.top, 25, 15, 15)
        bullets.add(bullet)
    def fire_2(self):
        ray = Bullet("123.png", self.rect.centerx - 10, self.rect.top, 50, 140, 15)
        rays.add(ray)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
  
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
bullets = sprite.Group()
rays = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)
 

finish = False
run = True 
rel_time = False
num_fire = 0
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and rel_time == False:
                    num_fire +=1
                    ship.fire()
                if num_fire >= 15 and rel_time == False:
                    last_time = timer()
                    rel_time == True

            elif e.key == K_e:
                if score % ray_fire == 0:
                    print(score // ray_fire)
                    ship.fire_2()
    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        rays.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        rays.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("ПЕРЕЗЯРЯДКА...", None, (150, 0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False 

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score += 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
        monsters.add(monster)

    collides1 = sprite.groupcollide(monsters, rays, True, False)
    for c in collides1:
        score += 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
        monsters.add(monster)

    if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        finish = True
        window.blit(lose, (200,200))
    if score >= goal:
        finish = True
        window.blit(win, (200,200))

    clock.tick(60)
    display.update()