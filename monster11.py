from pygame import *
from random import randint


# клас-шаблон для створення спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,size_x,size_y):
        super().__init__()
        # для збереження зображення спрайту
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed




        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y




    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))




# клас для головного персонажу
class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < width-60:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y < height-60:
            self.rect.y += self.speed
   
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top,10,15,20)
        bullets.add(bullet)


lost = 0
score = 0
shot = 0
mspeed = 2


class Monster(GameSprite):
    #рух ворога
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(20,width-70)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()








# розміри екрану
width = 800
height = 600


#підключення шрифтів
font.init()
font1 = font.SysFont("Arial",36)






# Створення персонажів гри
player = Player('rocket.png',350,height-60,5,80,100)


monsters = sprite.Group()
for i in range(1,5):
    monster = Monster('ufo.png',randint(20,width-70),0,mspeed,80,50)
    monsters.add(monster)






#Стоворення головного вікна
window = display.set_mode((width,height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(width,height))




game = True
clock = time.Clock()




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                shot += 1
   
    window.blit(background,(0,0))
    text_lose = font1.render('Пропущено: '+str(lost),1,(255,255,255))
    window.blit(text_lose,(10,20))
    text_shot = font1.render('Випущено пуль: '+str(shot),1,(255,255,255))
    window.blit(text_shot,(10,50))
    text_score = font1.render('Рахунок: '+str(score),1,(255,255,255))
    window.blit(text_score,(10,80))
    player.reset()
    player.move()


    monsters.update()
    bullets.update()


    monsters.draw(window)
    bullets.draw(window)


    if sprite.spritecollide(player,monsters,False):
        game = False



    if sprite.groupcollide(monsters,bullets,True,True):
        monster = Monster('ufo.png',randint(20,width-70),0,mspeed,80,50)
        monsters.add(monster)
        score += 1  


       
       






    display.update()
    clock.tick(60)

























