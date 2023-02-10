import numpy as np
import random

black, blue, green, red, white, yellow = 0, 1, 2, 3, 4, 5

colors = {"k": 0, "b": 1, "g": 2, "r": 3, "w": 4, "y": 5, "black": 0, "blue": 1, "green": 2, "red": 3, "white": 4, "yellow": 5}
words = {v: k for k, v in colors.items()}

def cost_string(costs):
    cost_s = ""
    cols = ["k", "b", "g", "r", "w"]
    for i in range(len(costs)):
        if costs[i] != 0:
            cost_s += str(costs[i]) + cols[i] + " "
    return cost_s


def import_cards():
    all_cards = {}
    rank1_deck, rank2_deck, rank3_deck = {}, {}, {}
    cards = open("splendor_cards.txt", "r").read()
    card_list = cards.split("\n")
    for card in card_list:
        props = card.split(",")
        if props[0].isnumeric():
            all_cards[int(props[0])] = Card(int(props[0]), int(props[1]), props[3], colors[props[2]],
                                            list(map(int, props[4:])))
            if int(props[1]) == 1:
                rank1_deck[int(props[0])] = Card(int(props[0]), int(props[1]), props[3], colors[props[2]],
                                                 list(map(int, props[4:])))
            elif int(props[1]) == 2:
                rank2_deck[int(props[0])] = Card(int(props[0]), int(props[1]), props[3], colors[props[2]],
                                                 list(map(int, props[4:])))
            elif int(props[1]) == 3:
                rank3_deck[int(props[0])] = Card(int(props[0]), int(props[1]), props[3], colors[props[2]],
                                                 list(map(int, props[4:])))

    return all_cards, [rank1_deck, rank2_deck, rank3_deck]


def import_nobles():
    all_nobles = {}
    nobles = open("splendor_nobles.txt", "r").read()
    noble_list = nobles.split("\n")
    for noble in noble_list:
        props = noble.split(",")
        if props[0].isnumeric():
            all_nobles[int(props[0])] = Noble(int(props[0]), list(map(int, props[1:])))
    return all_nobles


def draw_cards(deck, count):
    chosen = []
    for i in range(count):
        item_id, item = random.choice(list(deck.items()))
        del deck[item_id]
        chosen.append(item)
    return chosen


class Field(object):
    def __init__(self, deck_list):
        self.deck_list = deck_list

    def __repr__(self):
        return str(self.deck_list)

    def __len__(self):
        return len(self.deck_list)

    def id_in(self, card_id):
        for card in self.deck_list:
            if isinstance(card, Card):
                if card.get_id() == card_id:
                    return True
        return False

    def remove_id(self, card_id):
        for card in self.deck_list:
            if card.get_id() == card_id:
                self.deck_list.remove(card)

    def add_card(self, card):
        self.deck_list.append(card)


class Player(object):
    def __init__(self):
        self.gems = np.zeros(6)
        self.points = 0
        self.cards = np.zeros(5)
        self.nobles = []
        self.reserves = Field([])

    def get_points(self):
        return self.points

    def get_cards(self):
        return self.cards

    def get_gems(self):
        return self.gems

    def get_reserves(self):
        return self.reserves

    def set_gems(self, gem_list):
        self.gems = gem_list

    def set_cards(self, cards):
        self.cards = cards

    def can_buy_card(self, card):
        card_costs = card.get_costs()
        total = 0
        for i in range(len(card_costs)):
            total += max(0, card_costs[i] - self.gems[i] + self.cards[i])
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
            if gem in colors:
                gem = colors[gem]
            self.gems[int(gem)] += 1
        while sum(self.gems) > 10:
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
            if gem in colors:
                gem = int(colors[gem])
            print(gem)
            if gem < 0 or gem > 4 or not isinstance(gem, int):
                return False
            new_gems[int(gem)] += 1
        for j in range(len(new_gems)):
            if new_gems[j] > 2 or (new_gems[j] == 2 and game_gems[j] <= 4) or (game_gems[j] < new_gems[j]):
                return False
        return True

    def can_reserve_card(self):
        return len(self.reserves) < 3

    def reserve_card(self, card):
        self.reserves.add_card(card)
        return card

    def earned_noble(self, noble_list):
        earned = []
        for noble in noble_list:
            costs = noble.get_costs()
            can_buy = True
            for i in range(len(costs)):
                if costs[i] > self.cards[i]:
                    can_buy = False
            if can_buy:
                earned.append(noble)
        if len(earned) == 1:
            self.points += earned[0].get_points()
            return earned[0]
        if len(earned) > 1:
           while True:
                print("The following nobles are available:", earned)
                x = input("which noble would you like?")
                for noble in noble_list:
                    if noble.get_id() == int(x):
                        self.points += noble.get_points()
                        return noble
                print("Please enter a valid noble id")
        return None


class Card(object):
    def __init__(self, card_id, rank, points, color, costs):
        self.id = card_id
        self.points = int(points)
        self.color = color
        self.costs = list(map(int, costs))
        self.rank = rank

    def __repr__(self):
        return "ID:"+ str(self.id) + ", " + str(self.points) + "Pt, Col:" + words[
            self.color] + ", Costs:" + cost_string(self.costs)

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
    def __init__(self, noble_id, costs):
        self.id = noble_id
        self.costs = costs
        self.points = 3

    def __repr__(self):
        return "Noble: ID:" + str(self.id) + ", Costs:" + cost_string(self.costs)

    def get_costs(self):
        return self.costs

    def get_id(self):
        return self.id

    def get_points(self):
        return self.points


class Game(object):
    def __init__(self, num_players=2):
        self.player_list = []
        for num in range(num_players):
            self.player_list.append(Player())

        self.gems = np.array([6, 6, 6, 6, 6, 6])
        self.nobles = draw_cards(import_nobles(), num_players+1)
        self.all_cards, self.decks = import_cards()
        self.visible_cards = [Field(draw_cards(self.decks[0], 4)), Field(draw_cards(self.decks[1], 4)),
                              Field(draw_cards(self.decks[2], 4))]

    def play_game(self):
        while not self.game_over():
            for i in range(len(self.player_list)):
                player = self.player_list[i]
                action_taken = False
                while not action_taken:
                    for field in self.visible_cards:
                        print(field)
                    action = input(f"Player {i + 1}: (Take) Gems or (Buy) Card or (Reserve) Card")
                    if action.strip() == "Take":
                        gems = input("What gems would you like to take?").replace(" ", "").split(",")
                        if player.valid_take_gems(gems, self.gems):
                            gem_change = player.take_gems(gems)
                            for k in range(len(gem_change)):
                                self.gems[k] -= gem_change[k]
                            action_taken = True
                        else:
                            print("Not a valid gem selection")
                        print("Available Gems:", self.gems)
                    elif action.strip() == "Buy":
                        print(player.get_reserves())
                        card_to_buy = self.all_cards[int(input("Card ID"))]
                        rank_index = card_to_buy.get_rank() - 1
                        card_id = card_to_buy.get_id()
                        if player.can_buy_card(card_to_buy):
                            if self.visible_cards[rank_index].id_in(card_id):
                                self.visible_cards[rank_index].remove_id(card_id)
                                self.visible_cards[rank_index].add_card(draw_cards(self.decks[rank_index], 1))
                                player.default_buy_card(card_to_buy)
                                action_taken = True
                            elif player.get_reserves().id_in(card_id):
                                player.get_reserves().remove_id(card_id)
                                player.default_buy_card(card_to_buy)
                                action_taken = True
                    elif action.strip() == "Reserve":
                        if player.can_reserve_card():
                            print(self.visible_cards)
                            entry = input("Card ID or Rank to Draw (ex, R1")
                            if entry[0] == "R":
                                card_to_reserve = draw_cards(self.decks[int(entry[1]) - 1], 1)
                                player.reserve_card(card_to_reserve)
                                action_taken = True
                            elif entry.isnumeric():
                                card_to_reserve = self.all_cards[int(entry)]
                                player.reserve_card(card_to_reserve)
                                new_draw = draw_cards(self.decks[card_to_reserve.get_rank() - 1], 1)
                                self.visible_cards[card_to_reserve.get_rank() - 1].append(new_draw[0])
                                action_taken = True
                            else:
                                "Not a valid reservation choice"
                            if action_taken and player.valid_take_gems([yellow], self.gems):
                                gem_change = player.take_gems([yellow])
                                for k in range(len(gem_change)):
                                    self.gems[k] -= gem_change[k]
                        else:
                            print("Too many cards have been reserved")
                    noble = player.earned_noble(self.nobles)
                    if noble is not None:
                        self.nobles.remove(noble)

    def game_over(self):
        for player in self.player_list:
            if player.get_points() >= 15:
                return True
        return False

