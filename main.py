"""
Python 3.1.1
Pygame 1.9.1
Evheny Smirnov
"""

"""creating the screen"""
from livewires import games
import math
import random
"""creating the screen"""
games.init(screen_width = 1600, screen_height = 1020, fps = 50)

class Player_ship(games.Sprite):
    player_image = games.load_image("sprites/player_ship.bmp")
    ROTATION_STEP = 3
    def update(self):
        """movement of the ship"""
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Player_ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Player_ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 2
        if games.keyboard.is_pressed(games.K_s):
            self.y += 2
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 2
        if games.keyboard.is_pressed(games.K_d):
            self.x += 2
        if games.keyboard.is_pressed(games.K_SPACE): #shooting
            new_missle = Missle(self.x, self.y, self.angle)
            games.screen.add(new_missle)

class Enemy(games.Sprite):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL : games.load_image("sprites/enemy_SMALL.bmp"),
              MEDIUM : games.load_image("sprites/enemy_MEDIUM.bmp"),
              LARGE : games.load_image("sprites/enemy_LARGE.bmp") }
    SPEED = 2
    def __init__(self, x, y, size):
        """initializing sprite of an enemy ship"""
        super(Enemy, self).__init__(
            image = Enemy.images[size],
            x = x, y = y,
            dx = random.choice([1, -1]) * Enemy.SPEED * random.random()/size,
            dy = random.choice([1, -1]) * Enemy.SPEED * random.random() / size)
        self.size = size
    def update(self):
        if self.top == games.screen.height:
            self.destroy()
        if self.bottom == games.screen.height:
            self.destroy()
        if self.left == games.screen.width:
            self.destroy()
        if self.right == games.screen.width:
            self.destroy()

class Missle(games.Sprite):
    image = games.load_image("sprites/missle_player.bmp")
    BUFFER = 70 #distance from the ship
    LIFETIME = 100
    VELOCITY_FACTOR = 10 #speed
    def __init__(self, ship_x, ship_y, ship_angle):
        angle = ship_angle * math.pi/180
        """calculating the starting position of the missle"""
        buffer_x = Missle.BUFFER * math.sin(angle)
        buffer_y = Missle.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y
        dx = Missle.VELOCITY_FACTOR * math.sin(angle)
        dy = Missle.VELOCITY_FACTOR * -math.cos(angle)
        """creating the missle"""
        super(Missle, self).__init__(image = Missle.image,
                                     x = x, y = y,
                                     dx = dx, dy = dy)
        self.lifetime = Missle.LIFETIME
    def update(self):
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        if self.top == games.screen.height:
            self.destroy()
        if self.bottom == games.screen.height:
            self.destroy()
        if self.left == games.screen.width:
            self.destroy()
        if self.right == games.screen.width:
            self.destroy()

def main():
    space_background = games.load_image("pic/space.jpg", transparent=False )
    games.screen.background = space_background
    player_ship = Player_ship (image=Player_ship.player_image,
                               x=games.screen.width/2,
                               y=games.screen.height/2)
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Enemy.SMALL, Enemy.MEDIUM, Enemy.LARGE])
        new_enemy = Enemy(x = x, y = y, size = size)
        games.screen.add(new_enemy)
    games.screen.add(player_ship)
    games.screen.mainloop()

main()
