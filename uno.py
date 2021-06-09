print("uno.py started")

import copy
from random import shuffle
#Settings
player_num = 4
starting_card_num = 7
draw_1 = True

#Utilities
def print_deck(deck):
    print("Deck:")
    for card in deck:
        print(card.name)

def print_hand(player):
    print(f"Player {player.num}'s hand:")
    hand = []
    for card in player.hand:
        hand.append(card.name)
    print(hand)

#Core Classes
class Card:
    def __init__(self, color, num):
        self.color = color
        self.num = num
        self.name = self.color + " " + self.num

class Player:
    def __init__(self, num, cards, playstyle):
        self.num = num
        self.hand = cards
        self.playstyle = playstyle
    
    def get_most_color(self):
        card_count_dict = {'red':0,'yellow':0,'green':0,'blue':0}
        for card in self.hand:
            if card.color in card_count_dict:
                card_count_dict[card.color]+=1
        max_value = max(card_count_dict.values())
        max_keys = [color for color, value in card_count_dict.items() if value == max_value]
        return list(max_keys)[0]

    def play_card(self, deck, pile):
        #Organize hand so black cards are at the end and therefore other cards are prioritized
        #Put wilds with d4 following
        self.hand.sort(key=lambda s:s.name.startswith('black wild'))
        self.hand.sort(key=lambda s:s.name.startswith('black d4'))
        #Play cards
        if self.playstyle == 0:
            for card in self.hand:
                if card.color == pile[0].color or card.num == pile[0].num or card.color == 'black':
                    pile.append(card)
                    self.hand.remove(card)
                    print(f"Player {self.num} Playing Card: {card.name}")
                    return deck, pile
            if draw_1:
                print(f"Player {self.num} drawing card")
                deck, self.hand = draw_card(deck, self.hand)
                card = self.hand[-1]
                if card.color == pile[0].color or card.num == pile[0].num:
                    pile.append(card)
                    self.hand.remove(card)
                    print(f"Player {self.num} Playing Card: {card.name}")
                return deck, pile
            else:
                print(f"Player {self.num} drawing cards")
                while self.hand[-1].color != pile[0].color and self.hand[-1].num != pile[0].num:
                    deck, self.hand = draw_card(deck, self.hand)
                card = self.hand[-1]
                pile.append(card)
                self.hand.remove(card)
                print(f"Player {self.num} Playing Card: {card.name}")
                return deck, pile

#Main Functions
def draw_card(deck, player_hand):
    print(f"Drawing card: {deck[0].name}")
    player_hand.append(deck[0])
    deck.pop(0)
    return deck, player_hand

#Build Deck
def build_deck():
    deck = []

    colors = ['red', 'yellow', 'green', 'blue', 'black']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'd2', 'skip', 'rev']
    bnumbers = ['wild', 'wild', 'wild', 'wild', 'd4', 'd4', 'd4', 'd4']

    for color in colors:
        if color != 'black':
            for number in numbers:
                if number != '0':
                    deck.append(Card(color, number))
                deck.append(Card(color, number))
        else:
            for bnumber in bnumbers:
                deck.append(Card(color, bnumber))
        shuffle(deck)
    return deck

#Build Players
def build_players(deck, player_num, playstyles):
    players = []
    for player in range(player_num):
        player_hand = []
        for card_num in range(starting_card_num):
            deck, player_hand = draw_card(deck, player_hand)
        if player in playstyles:
            players.append(Player(player+1, player_hand, playstyles[player])) 
        else:
            players.append(Player(player+1, player_hand, 0))

    return players

def run(playstyles):
    current_player = 1
    deck = build_deck()
    players = build_players(deck, player_num, playstyles)
    #For Testing
    players[0].hand = [Card('black', 'wild'), Card('black', 'd4'), Card('red', 'skip'), Card('yellow', 'd2'), Card('green', 'rev'), Card('blue', '4')]
    #End For Testing
    pile = []
    deck, pile = draw_card(deck, pile)

    #play game
    #while(1):
    print(f"First card on pile: {pile[0].name}")
    print_hand(players[0])
    
    deck, pile = players[0].play_card(deck, pile)

    print_hand(players[0])

    if not players[current_player-1].hand:
        return print(f"{current_player} wins!")
    
    if current_player == player_num:
        current_player = 1
    else:
        current_player += 1
        
    


run({1:0})

print("uno.py finished")