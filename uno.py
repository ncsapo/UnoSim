print("uno.py started")

from random import shuffle
#Settings
player_num = 4

#Utilities
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

def draw_card(deck, player_hand):
    player_hand.append(deck[0])
    deck.pop(0)
    return deck, player_hand

def print_deck(deck):
    print("Deck:")
    for card in deck:
        print(card.name)

def print_hand(player):
    print(f"Player {player.num}'s hand:")
    for card in player.hand:
        print(card.name)

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
        for card_num in range(7):
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
    pile = []
    deck, pile = draw_card(deck, pile)

    #play game
    #while(1):

    print_hand(players[2])

    if not players[current_player-1].hand:
        return print(f"{current_player} wins!")
    
    if current_player == player_num:
        current_player = 1
    else:
        current_player += 1
        
    


run({2:1})

print("uno.py finished")