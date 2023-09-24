from pygame import *
init()

'''Необхідні класи'''
 
#клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
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
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):

    def update(self):
        if self.rect.x <= 70:
            self.direction = "right"

        if self.rect.x >= 600:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_haight):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.haight = wall_haight
        self.image = Surface((self.width, self.haight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Ігрова сцена:
win_width = 700
win_height = 500
 
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("bachmut.jpg"), (win_width, win_height))
 
#Персонажі гри:
player = Player('budanov.png', 10, win_height - 80, 5)
monster = Enemy('prigogin.png', win_width - 80, 280, 2)
final = GameSprite('boepripaci.png', win_width - 120, win_height - 80, 0)
 

walls = [
    Wall(7, 242, 76, 100, 20, 450, 10),
    Wall(7, 242, 76, 100, 480, 350,10),
    Wall(7, 242, 76, 100, 20, 10,380),
    Wall(7, 242, 76, 200, 130, 10,350),
    Wall(7, 242, 76, 450, 130, 10,360),
    Wall(7, 242, 76, 300, 20, 10,350),
    Wall(7, 242, 76, 390, 120, 130,10)

]

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
f = font.Font(None, 78)
win_text = f.render("YOU WIN!", True, (255, 215, 0))
lose_text = f.render("YOU LOSE!", True, (180,0,0))

#музика
mixer.init() # Створює музичний плеєр
mixer.music.load('kuku.mp3') # завантажує музику
mixer.music.play() # зациклює і програє її
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    

    if not finish:
        window.blit(background,(0, 0))
        player.reset()
        monster.reset()
        final.reset()
        for i in walls:
            i.reset()
            if player.rect.colliderect (monster.rect) or player.rect.colliderect(i.rect):
                finish=True
                window.blit(lose_text, (200, 200))
                mixer.music.stop()

        if player.rect.colliderect (final.rect):
                finish=True
                window.blit(win_text, (200, 200))
                mixer.music.stop()
        


        player.update()
        monster.update()

        display.update()
    clock.tick(FPS)
