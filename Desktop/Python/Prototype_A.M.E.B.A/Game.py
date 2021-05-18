import random
import sys
import pickle
import os


import pygame

import mod
import init

WIDTH = 700
HEIGHT = 600
FPS = 60

this_dir = os.getcwd()
img = this_dir + "/img/"
snd = this_dir + "/snd/"

print(this_dir)

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

icon = pygame.image.load(img + "icon.png")

# Создаем игру и окно
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game")
pygame.display.set_icon(icon)


clock = pygame.time.Clock()

# Загрузка всего
player_img = pygame.image.load(img + "player.png").convert()
block_img = pygame.image.load(img + "block.png").convert()
bonus_img = pygame.image.load(img + "bonus.png").convert()

background = pygame.image.load(img + "fons/fon_1.png")
background_rect = background.get_rect()

start_screen = pygame.image.load(img + "start_screen.png")

energy_img = pygame.image.load(img + "energy.png").convert()
energy_img.set_colorkey(BLACK)

energy_jump = pygame.image.load(img + "energy_jump.png").convert()
energy_jump.set_colorkey(BLACK)

react_img = pygame.image.load(img + "energy_react.png").convert()
react_img.set_colorkey(BLACK)

power_img = pygame.image.load(img + "energy_power.png").convert()
power_img.set_colorkey(BLACK)

pass_btn = pygame.image.load(img + "button/passive_button.png")
active_btn = pygame.image.load(img + "button/active_button.png")

pass_dead_btn = pygame.image.load(img + "button/passive_dead_button.png")
active_dead_btn = pygame.image.load(img + "button/active_dead_button.png")

money_img = pygame.image.load(img + "money_img.png").convert()
money_img.set_colorkey(BLACK)
money_max_img = pygame.transform.scale(money_img, (60, 60))

glasses_img = pygame.image.load(img + "Shmot/очки.png").convert()
glasses_img.set_colorkey(BLACK)

cap_img = pygame.image.load(img + "Shmot/cap.png")

#Загрузка музыки

main_theme = pygame.mixer.music.load(snd + "main.wav")

block_jump_snd = pygame.mixer.Sound(snd + "block_jump.wav")
block_down_snd = pygame.mixer.Sound(snd + "block_down.wav")

power_snd = pygame.mixer.Sound(snd + "power.wav")


energy_jump_snd = pygame.mixer.Sound(snd + "energy_jump.wav")
jump_error_snd = pygame.mixer.Sound(snd + "jump_error.wav")

money_1_snd = pygame.mixer.Sound(snd + "money_1.wav")
money_2_snd = pygame.mixer.Sound(snd + "money_2.wav")
money_sounds = [money_1_snd, money_1_snd]

btn_snd = pygame.mixer.Sound(snd + "button.wav")

if init.music:
    pygame.mixer.music.set_volume(init.music_volume)
    pygame.mixer.music.play(loops=-1)

def play_sound(snd):
    if init.sound:
        snd.set_volume(init.sound_volume)
        pygame.mixer.Sound.play(snd)


all_sprites = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
moneys = pygame.sprite.Group()


is_hits = False


class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (50,40))
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2

        self.count = 1
        self.speedx = 0
        self.speedy = 1
        self.is_jump = False
        self.counter = 0
        self.energy = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
      
        if self.is_jump:
            self.speedy = self.count
            if self.counter < 15:
                self.count -= 1
                self.counter += 1
            elif self.counter >=15:
                self.count += 1
                self.counter += 1
            if self.counter == 30:
                self.count = 1
                self.counter = 0
                self.is_jump = False
        
            
        self.rect.x += self.speedx
        
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(bonus_img, (50,50))
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x
    def update(self):
        if self.rect.x <= 0:
            self.kill()
class Money(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(money_img, (50, 50))
        

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    def update(self):
        if self.rect.x <= 0:
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y, image,speed):
        pygame.sprite.Sprite.__init__(self)


        self.width = random.randint(100,200)

        self.y = y
        self.x = x
        self.is_bonus = False
        self.speed = speed
        self.is_money = False
                
        self.image = pygame.transform.scale(image, (self.width, 30))
        self.image.set_colorkey(BLACK)
    
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-(self.width+self.x)

        self.rect.y = random.randint(self.y-100, self.y + 100)
        self.speedy = 0
        self.speedx = random.randint(speed//2, speed*2)

        if random.randint(1,2) == 2:
            self.speedx *= -1

        if self.speedx == 0:
                self.speedx = -3

        if self.speedx > 0:
            self.rect.x = 0
        
        
        if (random.randint(1,3)) == 1:
            
            if player.energy < 100:
                self.bonus = Bonus(self.rect.x + self.width//2,self.rect.y -50)
                all_sprites.add(self.bonus)
                bonuses.add(self.bonus)
                
                self.is_bonus = True
        if random.randint(1,10) == 1:
            self.money = Money(x = self.rect.x + self.width//2, y = self.rect.y - 50)
            moneys.add(self.money)
            all_sprites.add(self.money)
            self.is_money = True

       
        

    def update(self):
     
        if self.rect.x < 0-self.width or self.rect.left > WIDTH+self.width:
            
            
            if self.is_bonus:
                self.bonus.kill()
            if self.is_money:
                self.money.kill()
            
            self.__init__(self.x, self.y, self.image, self.speed)
            
            
        self.rect.x += self.speedx
        if self.is_bonus:  
            self.bonus.rect.x = self.rect.x + self.width//2
        if self.is_money:  
            self.money.rect.x = self.rect.x + self.width//2
             
        

blocks = pygame.sprite.Group()

player = Player(player_img)


def spawn(pos_x,pos_y, image,speed):
    for block in range (3):
        block = Block(pos_x, pos_y,image,speed)
        blocks.add(block)
        pos_y += 70
        pos_x += 40
spawn(0, 350, block_img, 3)


all_sprites.add(player)
all_sprites.add(blocks)
all_sprites.add(moneys)

levels = {1:"Иллюминатор"}


try:
    with open("save.txt", "rb") as f:
        level = pickle.load(f)
    with open("save_eq.txt", "rb") as f:
        products = pickle.load(f)
except:
    level = {"num":1,"name":"Иллюминатор","next":100,"speed": 3, "money" : 0, "score": 0}
    products = [["Очки", 10, 80, False],
                ["Шапка", 30, 160, False],
                ["Штаны", 70, 240, False]
                ]

def start_loop():

    start = True
    
    while start:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               start = False
           if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
               start = False
        screen.blit(start_screen,(0,0))       
        pygame.display.flip()

#Покупка
def pay(x):
    if level["money"] < x[1]:
        pass
    else:

        print(x)
        x[3] = True
        level["money"] -= x[1]

def passive():
    pass
#цикл магазина
def shop_loop():
    global shop
    shop = True

    def stop_shop():
        global shop

        shop = False


    while shop:



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)


        mod.Text(screen, "Shop", 130, 25, 36, None, (255,255,255))
        for product in products:
            if not(product[3]):
                if level["money"] >= product[1]:
                    mod.Button(master = screen,
                               text = product[0]+" за "+str(product[1]),
                               x = 200,
                               y = product[2],
                               pass_img = pass_btn,
                               active_img = active_btn,
                               color = GREEN,
                               sound=btn_snd,
                               command = lambda: pay(product))
                else:
                    mod.Button(master=screen,
                               text=product[0] + " за " + str(product[1]),
                               x=200,
                               y=product[2],
                               pass_img=pass_btn,
                               active_img=active_btn,
                               color=RED,
                               sound=btn_snd,
                               command=lambda: pay(product))
            else:
                mod.Button(master=screen,
                           text=product[0] + " за " + str(product[1]),
                           x=200,
                           y=product[2],
                           pass_img=pass_btn,
                           active_img=active_btn,
                           color= YELLOW,
                           sound=btn_snd,
                           command=passive)

        screen.blit(money_max_img, (WIDTH - 140, -8))
        mod.Text(master=screen,
                 text=str(level["money"]),
                 x=WIDTH - 80,
                 y=10,
                 color = (255,255,255))
        mod.Button(master=screen,
               text="Exit",
               x=200,
               y=300,
               pass_img=pass_btn,
               active_img=active_btn,
               sound=btn_snd,
               command=lambda: stop_shop())
        pygame.display.flip()


#цикл паузы
def pause_loop():

    pygame.mixer.music.pause()

    global pause
    pause = True
    def stop_pause():
        global pause
        pause = False
        pygame.mixer.music.unpause()
        

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)
        
        mod.Text(master = screen, text = "level: "+str(level["num"]), x = 100, y = 10, color = (255,255,255))
        mod.Text(master = screen, text = level["name"], x = WIDTH/2, y = 10, color = (255, 255, 255))

        mod.Button(master = screen,
        text = "Continue", 
        x = 200,
        y = 80, 
        pass_img = pass_btn,
        active_img = active_btn,
        sound=btn_snd,
        command = stop_pause)

        mod.Button(master = screen,
        text = "Exit", 
        x = 200,
        y = 240,
        pass_img = pass_btn, 
        active_img = active_btn,
        sound=btn_snd,
        command = lambda: sys.exit())

        mod.Button(master = screen,
                   text = "Shop",
                   x = 200,
                   y = 160,
                   pass_img = pass_btn,
                   sound=btn_snd,
                   active_img = active_btn,
                   command = shop_loop)
        screen.blit(money_max_img, (WIDTH - 140, -8))
        mod.Text(master=screen,
                 text=str(level["money"]),
                 x=WIDTH - 80,
                 y=10,
                 color = (255,255,255))

        pygame.display.flip()
start_loop()

react_jump = False
bonus = 0

def death_loop():

    global on_dead

    on_dead = True

    pygame.mixer.music.pause()
    level["score"] = 0

    def restart():
        player.rect.x = WIDTH//2
        player.rect.y = HEIGHT//2
        global on_dead
        on_dead = False
        print(on_dead)

    while on_dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(BLACK)

        mod.Button(master=screen,
                   text="Restart",
                   x=200,
                   y=160,
                   pass_img=pass_dead_btn,
                   sound=btn_snd,
                   active_img=active_dead_btn,
                   command=restart)



        pygame.display.flip()

# Цикл игры
running = True
while running:


    if level["num"]  > 1:
        background = pygame.image.load(img + "fons/fon_2.png")
        background_rect = background.get_rect()

    if level["score"] >= level["next"]:
        try:
            if level["num"]:
                level["name"] = levels[level["num"]]
        except:
            pass
       
        level["num"]+=1
        level["score"] = 0
        level["next"] = int(level["next"] *2)
        level["speed"] += 0.5
        for i in blocks:
            i.__init__(0,350,block_img, level["speed"])
           
        for i in bonuses:
            i.kill()
        for i in moneys:
            i.kill()
        player.__init__(player_img)
       

        
         

    
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)

    # ПРоверка умер л персонаж или нет?
    if player.rect.y > HEIGHT + 70:
        death_loop()

    hits = pygame.sprite.spritecollide(player, blocks, False)
    bonus_hits = pygame.sprite.spritecollide(player, bonuses, True)
    money_hits = pygame.sprite.spritecollide(player, moneys, True)

    if not(player.is_jump):
        react_jump = False
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            with open("save.txt", "wb") as f:
                pickle.dump(level, f)
            with open("save_eq.txt", "wb") as f:
                pickle.dump(products, f)
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_loop()
            if event.key == pygame.K_s:
                shop_loop()
            if event.key == pygame.K_SPACE:

                if not(hits):
                    if player.energy - 25 >= 0:
                        player.is_jump = True
                        player.energy -= 25
                        react_jump = True

                        play_sound(energy_jump_snd)
                    else:
                        play_sound(jump_error_snd)

                elif hits:
                    player.is_jump = True

                    play_sound(block_jump_snd)
                    

    if not(player.is_jump):
        player.speedy = 3
    if hits and not(player.is_jump):
        if not(is_hits):
            play_sound(block_down_snd)
        player.speedy = 0
        is_hits = True
    else:
        is_hits = False
    if bonus_hits:
        if player.energy + 25 <= 100:
            player.energy += 25
            bonus = 35
            play_sound(power_snd)
    if money_hits:
        level["money"] += 1
        play_sound(random.choice(money_sounds))


    player.rect.y += player.speedy

    level["score"] += 0.1
    
    
    # Обновление
    all_sprites.update()
    
    
    # Рендеринг
    screen.fill(WHITE)
    screen.blit(background, background_rect)

    all_sprites.draw(screen)

    for obj in products:
        if obj[3]:
            if obj[0] == "Очки":
                screen.blit(glasses_img, (player.rect.x, player.rect.y+7))
            if obj[0] == "Шапка":
                screen.blit(cap_img, (player.rect.x, player.rect.y-3))
    if player.is_jump and not(react_jump):
        screen.blit(energy_jump,(10,10))
    elif react_jump:
        screen.blit(react_img, (10,10))
    elif bonus:
        screen.blit(power_img, (10,10))
    else:
        screen.blit(energy_img, (10,10))
    

    
    screen.blit(money_max_img, (WIDTH-140, -8))

    mod.Text(screen, str(int(level["score"]))+"/"+str(level["next"]), WIDTH//2, 20)
    mod.Text(master = screen, text = str(level["money"]), x= WIDTH-80, y = 10)

    mod.Bar(master = screen,
            src = player.energy,
            width = 100,
            height = 10,
            x = 45,
            y = 17,
            fg = YELLOW,
            bg = WHITE
            
            )
    if bonus != 0:
        bonus -= 1       
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
