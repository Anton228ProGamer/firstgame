from pygame import *
from random import *

img_back = "galaxy.jpg"
img_hero = "rocket1.png"
img_enemy = "ufo.png" 
img_enemy2 = "asteroid.png"
img_bullet = "bullet.png"
font.init()
font2 = font.Font(None, 30)
font3 = font.Font(None, 250)
mixer.init()
mixer.music.load("Music.mp3")
mixer.music.play()

score = 0
lost = 0

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
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

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
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 1500
win_height = 800
display.set_caption("Шутер")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 6):
    monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters2.add(monster2)
ship = Player(img_hero, 5, win_height - 100, 80, 100, 50)

finish = False

run = True


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                ship.fire()

    if not finish:
        window.blit(background,(0,0))
        
        ship.update()
        ship.reset()
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        
        if sprite.spritecollide(ship, monsters, False) or lost >= 100:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 1000:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        lose = font3.render("Вы проиграли!   ", 1, (225, 225, 225))
        window.blit(text_lose, (10, 50))


        bullets.update()
        monsters.update()
        monsters2.update()
        monsters.draw(window)
        monsters2.draw(window)
        bullets.draw(window)
        
        
        display.update()
    time.delay(20)
