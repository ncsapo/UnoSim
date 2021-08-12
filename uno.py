print("uno.py started")

import copy
from random import shuffle
#Settings
player_num = 4
starting_card_num = 7
draw_1 = True
reversed = False
commentary =  False

#Utilities
def get_next_player(current_player):
    global reversed
    if not reversed:
        if current_player == player_num:
            current_player = 1
        else:
            current_player += 1
    else:
        if current_player == 1:
            current_player = player_num
        else:
            current_player -= 1
    return current_player

def print_deck(deck):
    if commentary:
        print("Deck:")
        for card in deck:
            print(card.name)

def print_hand(player):
    if commentary:
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
        max_value = max(list(card_count_dict.values()))
        max_keys = []
        max_keys.append([color for color, value in list(card_count_dict.items()) if value == max_value])
        return list(max_keys)[0]

    def play_card(self, deck, pile):
        #Organize hand so black cards are at the end and therefore other cards are prioritized
        #Put wilds with d4 following
        self.hand.sort(key=lambda s:s.name.startswith('black wild'))
        self.hand.sort(key=lambda s:s.name.startswith('black d4'))
        #Play cards
        if self.playstyle == 0:
            for card in self.hand:
                if card.color == pile[-1].color or card.num == pile[-1].num or card.color == 'black':
                    pile.append(card)
                    self.hand.remove(card)
                    if commentary: print(f"Player {self.num} Playing Card: {card.name}")
                    return deck, pile
            if draw_1:
                if commentary: print(f"Player {self.num} drawing card")
                deck, self.hand = draw_card(deck, self.hand)
                card = self.hand[-1]
                if card.color == pile[-1].color or card.num == pile[-1].num:
                    pile.append(card)
                    self.hand.remove(card)
                    if commentary: print(f"Player {self.num} Playing Card: {card.name}")
                return deck, pile
            else:
                if commentary: print(f"Player {self.num} drawing cards")
                while self.hand[-1].color != pile[-1].color and self.hand[-1].num != pile[-1].num:
                    deck, self.hand = draw_card(deck, self.hand)
                card = self.hand[-1]
                pile.append(card)
                self.hand.remove(card)
                if commentary: print(f"Player {self.num} Playing Card: {card.name}")
                return deck, pile

#Main Functions
def draw_card(deck, player_hand, *pile):
    if len(deck) == 0:
        if commentary: print("Reshuffling Pile into new Deck")
        deck, pile = rebuild_deck(pile)
        if commentary: print(f"Deck is now {deck} and pile is now {pile}")
    if commentary: print(f"Drawing card: {deck[0].name}")
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

def rebuild_deck(pile):
    deck = copy.deepcopy(pile[:-1])
    pile = [pile[-1]]
    shuffle(deck)
    print(f"Deck is {deck}")
    return deck, pile

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
    if commentary: (f"First card on pile: {pile[-1].name}")
    while(1):
    #for times in range(50):    
        print_hand(players[current_player-1])
    
        deck, pile = players[current_player-1].play_card(deck, pile)

        print_hand(players[current_player-1])

        if commentary: print(f"Card on top of pile: {pile[-1].name}")

        if not players[current_player-1].hand:
            if commentary: print(f"Player {current_player} wins!")
            return current_player
    
        #Special Cards
        if pile[-1].num == 'rev':
            global reversed
            if not reversed: 
                reversed = True
            else: 
                reversed = False
            if commentary: print("Play is reversed!")

        if pile[-1].num == 'skip':
            current_player = get_next_player(current_player)   
            if commentary: print(f"Player {current_player} is skipped!")   

        if pile[-1].num == 'd2':
            current_player = get_next_player(current_player)
            if commentary: print(f"Player {current_player} is drawing 2")
            draw_card(deck, players[current_player-1].hand, pile)
            draw_card(deck, players[current_player-1].hand, pile)
            print_hand(players[current_player-1])

        if pile[-1].color == 'black':
            new_color = players[current_player-1].get_most_color()[0]
            pile[-1].color = new_color
            if commentary: print(f"The new color is: {new_color}!")

            if pile[-1].num == 'd4':
                current_player = get_next_player(current_player)
                if commentary: print(f"Player {current_player} is drawing 4")
                draw_card(deck, players[current_player-1].hand, pile)
                draw_card(deck, players[current_player-1].hand, pile)
                draw_card(deck, players[current_player-1].hand, pile)
                draw_card(deck, players[current_player-1].hand, pile)
                print_hand(players[current_player-1])

        current_player = get_next_player(current_player)
        #Reshuffle Pile is deck runs out
        if len(deck) == 0:
            if commentary: print("Reshuffling Pile into new Deck")
            deck, pile = rebuild_deck(pile)
            print(f"Deck is now {deck} and pile is now {pile}")
        if commentary: print("\n")


#run({1:0})

if commentary: print("uno.py finished")

#Tuple Error