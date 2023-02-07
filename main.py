import numpy as np

red, blue, white, green, black, yellow = 0, 1, 2, 3, 4, 5


class Player(object):
    def __init__(self):
        self.gems = np.zeros(6)
        self.points = 0
        self.cards = np.zeros(5)
        self.nobles = []

    def get_points(self):
        return self.points

    def get_cards(self):
        return self.cards

    def get_gems(self):
        return self.gems

    def set_gems(self, gem_list):
        self.gems = gem_list

    def can_buy_card(self, card):
        card_costs = card.get_costs()
        total = 0
        for i in range(len(card_costs)):
            total += max(0, card_costs[i] - self.gems[i] + self.cards[i])
            print(total)
        return total <= self.gems[yellow]

    def default_buy_card(self, card):
        card_costs = card.get_costs()
        returns = np.zeros(6)
        wild = 0
        if self.can_buy_card(card):
            for i in range(len(card_costs)):
                wild += max(0, self.gems[i] + self.cards[i] - card_costs[i])
                returns[i] = max(0, card_costs[i] - self.cards[i])
                self.gems[i] -= returns[i]
            self.gems[yellow] -= wild
            returns[yellow] = wild
            self.cards[card.get_color()] += 1
            self.points += card.get_points()
        return returns

    def take_gems(self, gem_list):
        original_gems = self.gems.copy()
        for gem in gem_list:
            self.gems[int(gem)] += 1
        if sum(self.gems) > 10:
            returns = input(f'Please Return {sum(self.gems) - 10} gems')
            for gem in returns:
                self.gems[gem] -= 1
        print("Player ", self.gems)
        return self.gems - original_gems

    def valid_take_gems(self, gem_list, game_gems):
        if len(gem_list) > 3:
            return False
        new_gems = np.zeros(6)
        for gem in gem_list:
            new_gems[int(gem)] += 1
        for j in range(len(new_gems)):
            if new_gems[j] > 2 or (new_gems[j] == 2 and game_gems[j] <= 4) or (game_gems[j] < new_gems[j]):
                return False
        return True

class Card(object):
    def __init__(self, id, rank, points, color, costs):
        self.id = id
        self.points = points
        self.color = color
        self.costs = costs
        self.rank = rank

    def __print__(self):


    def get_points(self):
        return self.points

    def get_color(self):
        return self.color

    def get_costs(self):
        return self.costs

    def get_rank(self):
        return self.rank

    def get_id(self):
        return self.id

class Noble(object):
    def __init__(self, costs):
        self.costs = costs

    def get_costs(self):
        return self.costs


class Game(object):
    def __init__(self):
        self.player_list = [Player(), Player()]
        self.gems = np.array([6, 6, 6, 6, 6, 6])
        self.visible_cards = np.zeros([3, 4])
        self.card_dict = {1: Card(0, 1, 2, 1, [0, 0, 1, 2, 0])}
        self.visible_cards[0, 0] = 1


    def play_game(self):
        while not self.game_over():
            for i in range(len(self.player_list)):
                action_taken = False
                while not action_taken:
                    action = input(f"Player {i+1}: (Take) Gems or (Buy) Card")
                    if action.strip() == "Take":
                        gems = input("What gems would you like to take?").split(",")
                        if self.player_list[i].valid_take_gems(gems, self.gems):
                            gem_change = self.player_list[i].take_gems(gems)
                            print("Gem Change", gem_change)
                            for k in range(len(gem_change)):
                                self.gems[k] -= gem_change[k]
                            action_taken = True
                        else:
                            print("Not a valid gem selection")
                        print("Available Gems:", self.gems)
                    elif action.strip() == "Buy":
                        print(self.visible_cards)
                        test_card = self.card_dict[self.visible_cards[0][0]]
                        if self.player_list[i].can_buy_card(test_card):
                            print("Can Buy Card")

    def game_over(self):
        for player in self.player_list:
            if player.get_points() >= 15:
                return True
        return False


def test_player_take_gems():
    new_player = Player()
    print(new_player.get_gems())
    new_player.take_gems([0, 2, 3])
    print(new_player.get_gems())


def test_game_take_gems():
    new_game = Game()
    new_game.play_game()


def test_card_purchase():
    test_card = Card(0, 1, 2, 1, [0, 0, 1, 2, 0])
    new_player = Player()
    new_player.set_gems([0, 1, 2, 2, 2, 0])
    x = new_player.can_buy_card(test_card)
    print(x)

# test_game_take_gems()
test_card_purchase()