#подключение библиотек
from pygame import *
from random import randint
#музыка
font.init()
mixer.init()
mixer.music.load('mus.mp3')
mixer.music.play(-1)
#создай окно игры
window = display.set_mode((1000,700))
display.set_caption('Arcane')

#задай фон сцены
backgroung = transform.scale(
    image.load('gamefon.jpg'),
    (1000,700)
)
background1 = transform.scale(
    image.load('menfon.jpg'),
    (1000,700)
)



class Area():
 #создание прямоугольника   
    def __init__(self, x, y, whide, heidht, color):
        self.fill_color = color
        self.rect = Rect(x, y, whide, heidht)
#Заданный цвет  прямоугольника
    def set_color(self,color):
        self.fill_color = color
#Рисует прямоугольник
    def fill(self):
        draw.rect(window, self.fill_color, self.rect)
        #проверка столкновения
    def collidepoint(self, x, y):
            return self.rect.collidepoint(x,y)
    #рамочка
    def draw_stroke(self,color,trikkes):
        draw.rect(window, color, self.rect, trikkes)
# создает прмоугольник с надписью
class Label(Area):
    def __init__ (self,x,y, whide, heidht, color):
        super().__init__(x, y , whide, heidht, color)

    def set_text(self,fsize, text, text_color):
        font1 = font.SysFont('verdana', fsize)
        self.image = font1.render(text, True, text_color)
# рисует карточку вместе с текстом
    def draw(self, shift_x, shift_y):
        self.fill()
        window.blit(self.image,(self.rect.x + shift_x, self.rect.y + shift_y))
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x ,y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x>=0:
            self.rect.x -= 5
        if keys_pressed[K_RIGHT] and self.rect.x<=1300:
            self.rect.x += 5
    def fire(self):
        bullet = Bullet('hec.png',140,100,5, self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global propusk
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(0,600)
            propusk += 1
        
class Bullet(GameSprite):
    global killi
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

card = Label(320,400,350,100,(136,126,116))
card2 = Label(380,470,250,100,(0,0,0))
card.set_text(50, "Начать игру",(255,255,255))
card2.set_text(40, "Return",(255,255,255))
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 45)
win =  font1.render('Все кончено, Джейс', True , (108,0,15))
deaad =  font1.render("Это еще не конец" , True , (108,0,15))
retur = font2.render('Нажмите R чтобы перезапустить', True , (255,255,255))
clock = time.Clock()
#персонажи
def init_game():
    global player, monsters,bullets,propusk,killi,game,finish,menu,restart
    player = Player('victor.png', 170, 200, 10, 100, 600 )
    zlodei = Enemy('jace.png',150,200,1,35,0)
    zlodei2 = Enemy('jace.png',85,85,2,355,0)
    zlodei3 = Enemy('jace.png',100,100,1,567,0)
    zlodei4 = Enemy('jace.png',150,150,1,723,0)
    zlodei5 = Enemy('jace.png',150,140,1,180,0)
    monsters = sprite.Group()
    monsters.add(zlodei,zlodei2,zlodei3,zlodei4,zlodei5)
    
    bullets = sprite.Group()
    #подключение надписей
    global moneti
    moneti = 0
    propusk = 0
    killi = 0
    game = True
    finish = True
    menu = True
    restart = False
init_game()
while game:
    if menu:
        window.blit(background1, (0,0))
        card.draw(20,20)
            # событие нажатие мыщи
        for ev in event.get():
            if ev.type == QUIT:
                game = False
            if ev.type == MOUSEBUTTONDOWN:
                x,y = ev.pos
                if card.collidepoint(x,y):
                    finish = False
                    menu = False
        # display.update()
    if finish == False:
        propsk = font2.render('Промах: ' + str(propusk) , True , (93,1,164))
        kills = font2.render('Убит: ' + str(killi) , True , (93,1,164 ))
        monets = font2.render('Собрано монет: ' + str(moneti) , True , (93,1,164 ))
        window.blit(backgroung, (0,0))
        window.blit(propsk,(760,10))
        window.blit(kills, (10,10))
        window.blit(monets, (300,10))
        monsters.draw(window)
        bullets.draw(window)
        player.reset()
        bullets.update()
        monsters.update()
        player.update()
        
        monsters_list = sprite.groupcollide(monsters,bullets, True, True)
        for monster in monsters_list:
            killi += 1
            moneti += 1
            zlodei6 = Enemy('jace.png',150,150, randint(1,2),randint(0,635),0)
            monsters.add(zlodei6)

        if killi >= 30:
            finish = True
            window.blit(win,(190,280))
            window.blit(retur,(170,400))
        if propusk >= 6:
            finish = True
            window.blit(retur,(170,400))
            window.blit(deaad,(230,280))



        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
            if e.type == KEYDOWN:
                if e.key == K_r:  # Перезапуск при нажатии 'R'
                    init_game()
    #                 restart = True
    #                 finish = True
    # if restart:
    #     #персонажи
    #     player = Player('image.png', 120, 120, 10, 100, 600 )
    #     zlodei = Enemy('asteroid.png',65,65,1,35,0)
    #     zlodei2 = Enemy('asteroid.png',85,85,2,355,0)
    #     zlodei3 = Enemy('asteroid.png',100,100,1,567,0)
    #     zlodei4 = Enemy('asteroid.png',90,90,1,723,0)
    #     zlodei5 = Enemy('asteroid.png',85,85,1,180,0)
    #     monsters = sprite.Group()
    #     monsters.add(zlodei,zlodei2,zlodei3,zlodei4,zlodei5)
    #     card = Label(40,150,290,100,(0,0,0))
    #     card2 = Label(380,470,250,100,(0,0,0))
    #     card.set_text(40, "New game",(255,255,255))
    #     card.set_text(40, "Return",(255,255,255))
    #     bullets = sprite.Group()
    #     #подключение надписей
    #     font1 = font.Font(None, 70)
    #     font2 = font.Font(None, 45)
    #     win =  font1.render('6 Am', True , (255,0,0))
    #     deaad =  font1.render('YOU DEAD', True , (255,0,0))
    #     clock = time.Clock()
    #     propusk = 0
    #     killi = 0

    if finish == True and menu == False:            
        for e in event.get():
            if e.type == QUIT:
                game = False
        if e.type == KEYDOWN:
            if e.key == K_r:  # Перезапуск при нажатии 'R'
                init_game()
    clock.tick(130)
    display.update()
