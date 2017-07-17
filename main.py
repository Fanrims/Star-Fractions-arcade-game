"""
Python 3.1.1
Pygame 1.9.1
Evgeny Smirnov
"""

from livewires import games, color
import math
import random

games.init(screen_width = 1600, screen_height = 1020, fps = 50) # screen

class Ship(games.Sprite):
    """main class of all ships"""
    def update(self):
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width

    def attack(self):
        new_missle = Missle(self.x, self.y, self.angle)
        games.screen.add(new_missle)

class Player(Ship):
    def __init__(self, game, x, y):
        """initialize sprite"""
        super(Player, self).__init__(image = Player.player_image, x=x, y=y)
        self.game = game
    player_image = games.load_image("sprites/player_ship.bmp")
    ROTATION_STEP = 3
    MISSLE_DELAY = 20
    HP = 5
    missle_wait = 0

    def update(self):
        super(Player, self).update()
        """movement of the ship"""
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Player.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Player.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 2
        if games.keyboard.is_pressed(games.K_s):
            self.y += 2
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 2
        if games.keyboard.is_pressed(games.K_d):
            self.x += 2
        if games.keyboard.is_pressed(games.K_SPACE) and self.missle_wait == 0:# shooting
            self.attack()
            self.missle_wait = Player.MISSLE_DELAY
        if self.missle_wait > 0:
            self.missle_wait -= 1
        if self.overlapping_sprites:
            self.HP -= 1
            self.game.hit_points.value -= 1
            self.game.hit_points.right = games.screen.width - 10
            for Enemy in self.overlapping_sprites:
                Enemy.die()
            if self.HP == 0:
                for sprite in self.overlapping_sprites:
                    sprite.die()
                self.die()

    def die(self):
        """destroy ship"""
        self.destroy()
        self.game.end()

class Enemy(Ship):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    POINTS = 100

    images = {SMALL : games.load_image("sprites/enemy_SMALL.bmp"),
              MEDIUM : games.load_image("sprites/enemy_MEDIUM.bmp"),
              LARGE : games.load_image("sprites/enemy_LARGE.bmp") }
    SPEED = 2
    count = 0

    MISSLE_DELAY = 20
    missle_wait = 0

    def __init__(self, game, x, y, size):
        """initialize sprite of an enemy ship"""
        Enemy.count += 1
        super(Enemy, self).__init__(
            image = Enemy.images[size],
            x = x, y = y,
            dx = random.choice([1, -1]) * Enemy.SPEED * random.random()/size,
            dy = random.choice([1, -1]) * Enemy.SPEED * random.random() / size)
        self.size = size
        self.game = game

    def update(self):
        super(Enemy, self).update()
        if self.overlapping_sprites == Missle.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()
        while Player.HP > 0 and self.missle_wait == 0: #shiiiiieeet
            self.attack()
            self.missle_wait = Enemy.MISSLE_DELAY

    def die(self):
        self.game.score.value += int(Enemy.POINTS * self.size)
        self.game.score.right = games.screen.width - 10
        Enemy.count -= 1
        if Enemy.count == 0:
            self.game.newLevel()
        self.destroy()

class Missle(games.Sprite):
    image = games.load_image("sprites/missle_player.bmp")
    BUFFER = 130 #distance from the ship
    LIFETIME = 100
    VELOCITY_FACTOR = 10 #speed

    def __init__(self, ship_x, ship_y, ship_angle):
        angle = ship_angle * math.pi/180
        """calculate the start position of the missle"""
        buffer_x = Missle.BUFFER * math.sin(angle)
        buffer_y = Missle.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y
        dx = Missle.VELOCITY_FACTOR * math.sin(angle)
        dy = Missle.VELOCITY_FACTOR * -math.cos(angle)
        """create missle"""
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
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
            self.destroy()

class Game(object):
    def __init__(self):
        self.level = 0
        """initialize an object Game"""
        #add score and player hit points
        self.score = games.Text(value = 0,
                                size = 50,
                                color = color.white,
                                top = 10,
                                right = games.screen.width - 10,
                                is_collideable=False)
        self.hit_points = games.Text(value=Player.HP,
                                     size = 50,
                                     color=color.white,
                                     top=70,
                                     right=games.screen.width - 10,
                                     is_collideable=False)
        games.screen.add(self.score)
        games.screen.add(self.hit_points)
        #create player
        self.Player = Player(game = self,
                                       x = games.screen.width / 2,
                                       y = games.screen.height / 2)
        games.screen.add(self.Player)

    def play(self):
        """start the game"""
        games.music.load("sounds/StarFr_title.mp3")
        games.music.play(-1)
        background = games.load_image("pic/space.jpg")
        games.screen.background = background
        #start with level 1
        self.newLevel()
        games.screen.mainloop()

    def newLevel(self):
        self.level += 1
        BUFFER = 150

        for i in range(self.level * 2):
            # calculate distance around player and spawn 8 enemies
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)
            x = self.Player.x + x_distance
            y = self.Player.y + y_distance
            x %= games.screen.width  # return an enemy into the screen
            y %= games.screen.height  # if it spawn out of it
            enemies = Enemy(game=self,
                            x=x,
                            y=y,
                            size=random.choice([Enemy.SMALL, Enemy.MEDIUM, Enemy.LARGE]))
            games.screen.add(enemies)



    def end(self):
        end_massage = games.Message(value= "GAME OVER",
                                    size = 300,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y =games.screen.height/2,
                                    lifetime= 5*games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_massage)

def main():
    star_fraction = Game()
    star_fraction.play()
main()