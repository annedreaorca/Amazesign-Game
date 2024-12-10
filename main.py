from game import Game
from GestureScreen import GestureScreen

g = Game()

while g.running:
    g.curr_menu.display_menu()

    if g.playing:
        # Pass the Game instance to GestureScreen
        gesture_screen = GestureScreen(g)
        while gesture_screen.running:
            gesture_screen.display()

        g.playing = False

    g.game_loop()
