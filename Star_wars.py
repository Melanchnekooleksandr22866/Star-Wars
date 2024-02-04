from pygame import *
from random import randint

mixer.init()
mixer.music.load("nachalo.mp3")
mixer.music.play()
fire_sound = mixer.Sound("laser.mp3")

goal = 51
lost = 0
score = 0
max_lost = 6

win_width = 700
win_height = 500

font.init()
font1 = font.Font(None, 80)
win_text = font1.render('    You Win!!!', True, (0, 255, 0))
lose_text = font1.render('               You Lose!!!', True, (250, 0, 0))
font2 = font.Font(None, 36)

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

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("pyli.png", self.rect.centerx, self.rect.top, 15, 40, -25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost = lost + 1

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40

player = Player("raketa.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("monsters.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

meteors = sprite.Group()
for i in range(1, 6):
    meteor = Meteor("meteor.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    meteors.add(meteor)

init() 

background = transform.scale(image.load("background.jpg"), (win_width, win_height))
loading_screen = transform.scale(image.load("nachalo.png"), (win_width, win_height))

window = display.set_mode((win_width, win_height))
window.blit(loading_screen, (0, 0))
loading_text = font2.render("Привіт, у мене є місія для тебе", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 175, win_height - 350))
loading_text = font2.render("на нашу базу напали сітхи", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 300))
loading_text = font2.render("і ти повинен відбити 50 кораблів", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 190, win_height - 250))
loading_text = font2.render("щоб перемогти!", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 100, win_height - 200))
loading_text = font2.render("Натисни на E, щоб почати гру", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 175, win_height - 50))
display.update()

game = True
finish = False
game_started = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_e and not game_started:
                mixer.music.load("rise.mp3")
                mixer.music.play(-1)
                game_started = True
                finish = False
                window.blit(background, (0, 0))
                display.update()
            elif e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if game_started:
        if not finish:
            window.blit(background, (0, 0))

            text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))

            text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lost, (10, 50))

            player.update()
            monsters.update()
            meteors.update()
            bullets.update()

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score = score + 1
                monster = Enemy("monsters.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

            monsters.draw(window)
            meteors.draw(window)
            bullets.draw(window)
            player.reset()

            display.update()

            if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, meteors, True):
                lost = lost + 2

            if score >= goal:
                finish = True
                window.blit(win_text, (win_width // 2 - 200, win_height // 2 - 50))
                display.update()
                time.delay(2500)
                game = False

            if lost >= max_lost:
                finish = True
                window.blit(lose_text, (win_width // 3 - 250, win_height // 2 - 50))
                display.update()
                time.delay(2500)
                game = False

    time.delay(50)
