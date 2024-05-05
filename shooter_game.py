#Создай собственный Шутер!
from random import randint
from pygame import *

global bullets
bullets = sprite.Group()
global score
score=0
class GameSprite(sprite.Sprite):

   #конструктор класса

    def __init__(self, player_image, player_x, player_y, player_speed):

        super().__init__()

       # каждый спрайт должен хранить свойство image - изображение

        self.image = transform.scale(image.load(player_image), (65, 65))

        self.speed = player_speed

       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан

        self.rect = self.image.get_rect()

        self.rect.x = player_x

        self.rect.y = player_y

 

    def reset(self):

        window.blit(self.image, (self.rect.x, self.rect.y))

 

#класс-наследник для спрайта-игрока (управляется стрелками)

class Player(GameSprite):

    def update(self):

        keys = key.get_pressed()

        if keys[K_a] and self.rect.x > 5:

            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_width - 80:

            self.rect.x += self.speed
        
        if keys[K_LEFT] and self.rect.x > 5:

            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < win_width - 80:

            self.rect.x += self.speed
        if keys[K_SPACE]:
            global bullets
            bullets.add([Bullet('bullet.png', self.rect.x, self.rect.y, 4)])


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            bullet.kill()
lost = 0

score = 0

class Enemy(GameSprite): 
    def __init__(self, player_image, player_x, player_y, player_speed):

        super().__init__(player_image, player_x, player_y, player_speed)
        self.lifes = 1

    def update(self):
        if self.lifes:
            self.rect.y += self.speed
            global lost
            global monsters
            global bullets
            global score   
            if self.rect.y >= 600:
                self.__init__("ufo.png", randint(80, win_height - 80), -40,  randint(1,5))
                lost = lost + 1
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score = score + 1
                c.kill()
                c.lifes = 0
                c.rect.y =1000000
                monster = Enemy("asteroid.png", randint(80, win_width - 80), -40, 5)
                
                monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)


win_width = 700

win_height = 500

player = Player('rocket.png', 5, win_height - 80, 4)

bullet = Bullet('bullet.png', 5, win_height - 80, 4)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_height - 80), -40,  randint(1,5))
    monsters.add(monster)
window = display.set_mode((win_width, win_height))

display.set_caption("Maze")

background = transform.scale(image.load("144.png"), (win_width, win_height))

game = True

finish = False

clock = time.Clock()

FPS = 60

mixer.init()

mixer.music.load('155.ogg')

mixer.music.play()


while game:

    for e in event.get():

        if e.type == QUIT:

            game = False

    if finish != True:
            
        window.blit(background,(0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(30,30))
        text_lose = font1.render('СЧЁТ:' + str(score), 1, (255, 255, 255))
        window.blit(text_lose,(30,90))
        win = font1.render('You win', True, (255, 215, 0))
        player.update()
        player.reset()

        for bullet in bullets:
            bullets.update()
            bullets.draw(window)

            bullet.reset()
        
        for monster in monsters:
            monster.update()
            monster.reset()

        display.update()

        clock.tick(FPS)