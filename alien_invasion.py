"""file that starts game"""

import event_handler


def run_game():
    game = event_handler.SpaceInvaders()
    game.main()


run_game()
