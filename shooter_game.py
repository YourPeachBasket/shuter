from pygame import *
from random import randint
from time import sleep, time as timer
window = display.set_mode((700, 500))
clock = time.Clock()
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
lostsound = mixer.Sound('lostgame1.mp3')
winsound = mixer.Sound('winsound.ogg')
# класс-родитель для других спрайтов


class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока


class Player(GameSprite):
    def update(self):
        speed = 10
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= speed
        if keys_pressed[K_RIGHT] and self.rect.x < 605:
            self.rect.x += speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top-16, 15, 20, 7)
        bullets.add(bullet)
        fire.play()


lost = 0
font.init()
font1 = font.Font(None, 26)
font2 = font.Font(None, 80)


class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 620)
            self.speed = randint(1, 3)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()


game = True
finish = False
hero = Player('rocket.png', 20, 390, 80, 100, 8)
monsters = sprite.Group()
for monster in range(5):
    monster = Enemy('ufo.png', randint(5, 620), 0, 80, 50, randint(1, 3))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for asteroid in range(3):
    asteroid = Enemy('asteroid.png', randint(5, 620), 0, 80, 50, randint(1, 3))
    asteroids.add(asteroid)
win = 0
num_fire = 0
rel_time = False
while game:
    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_win = font1.render("Пoвержено: " + str(win), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        window.blit(text_win, (10, 30))
        bullets.draw(window)
        bullets.update()
        sprites_list = sprite.spritecollide(hero, monsters, False)
        sprites_list1 = sprite.spritecollide(hero, asteroids, False)
        collide = sprite.groupcollide(monsters, bullets, True, True)
        for i in collide:
            win += 1
            monster = Enemy('ufo.png', randint(5, 620),
                            0, 100, 50, randint(1, 3))
            monsters.add(monster)
        if sprites_list or lost >= 10:
            finish = True
            lose = font2.render("YOU LOST", 1, (255, 0, 0))
            window.blit(lose, (200, 200))
            lostsound.play()
        if win >= 10:
            finish = True
            win = font2.render("YOU WON", 1, (0, 255, 0))
            window.blit(win, (200, 200))
            winsound.play()
    else:
        sleep(5)
        lost = 0
        win = 0
        for monster in monsters:
            monster.kill()
        for bullet in bullets:
            bullet.kill()
        for monster in range(5):
            monster = Enemy('ufo.png', randint(5, 620),
                            0, 100, 50, randint(1, 3))
            monsters.add(monster)
        finish = False
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5:
                    hero.fire()
                    num_fire += 1
                else:
                    rel_time = True
                    timenow = timer()
    if rel_time == True:
        timenow2 = timer()
        if timenow2-timenow < 3:
            reload = font1.render('Wait, reload', 1, (255, 0, 0))
            window.blit(reload, (280, 480))
        else:
            num_fire = 0
            rel_time = False

    if e.type == QUIT:
        game = False
    clock.tick(50)
    display.update()
