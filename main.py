"""
Python 3.1.1
pygame 1.9.1
"""

"""creating the screen"""
from livewires import games
games.init(screen_width = 1600, screen_height = 900, fps = 50)

def main():
    space_background = games.load_image("pic/space.jpg" , transparent = False )
    games.screen.background = space_background
    games.screen.mainloop()
main()

