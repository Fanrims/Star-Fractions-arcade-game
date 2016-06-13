"""
Python 3.1.1
pygame 1.9.1
"""
from livewires import games
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
            self.y -= 1
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1

def main():
    space_background = games.load_image("pic/space.jpg", transparent=False )
    games.screen.background = space_background
    player_ship = Player_ship (image=Player_ship.player_image,
                               x=games.screen.width/2,
                               y=games.screen.height/8)
    games.screen.add(player_ship)
    games.screen.mainloop()

main()

