from main import *


def test_player_take_gems():
    new_player = Player()
    print(new_player.get_gems())
    new_player.take_gems(["k", "r", "w"])
    print(new_player.get_gems())


def play_game():
    new_game = Game()
    new_game.play_game()


def test_card_purchase():
    test_card = Card(0, 1, 2, 1, [0, 0, 1, 2, 0])
    new_player = Player()
    new_player.set_gems([0, 1, 2, 2, 2, 0])
    x = new_player.can_buy_card(test_card)
    print(x)


def test_import_cards():
    all_cards, decks = import_cards()
    for card in all_cards:
        print(all_cards[card])


def test_import_nobles():
    all_nobles = import_nobles()
    noble_list = draw_cards(all_nobles, 3)
    print(noble_list)
    for noble in noble_list:
        print(noble)


play_game()
# test_player_take_gems()
