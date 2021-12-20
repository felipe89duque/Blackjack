import numpy as np
import random

class Card:

    def __init__(self,name,suit):
        self.name = name
        self.value = self.__get_value(name)
        self.suit = suit

    def __get_value(self,name):
        try:
            value = int(name)
        except: # name cannot be converted to int, then it's A,J,Q or K
            if name == 'A':
                value = None
            else:
                value = 10
        return value

class Decks:
    
    def __init__(self,number_of_decks = 0):
        
        if number_of_decks == 0: # Create only 1 deck, but re-stack it after each action
            number_of_decks = 1
            self.restack = True
        else:
            self.restack = False

        suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
        non_numeric_cards = ["J", "Q", "K", "A"]

        self.cards = np.empty((number_of_decks,len(suits),13),dtype = Card)

        for i in range(number_of_decks):
            for k in range(len(suits)):
                for j in range(9): # Cards with numeric name
                    self.cards[i,k,j] = Card(j+2,suits[k])
                for j in range(9,13): # Cards with non-numeric name
                    self.cards[i,k,j] = Card(non_numeric_cards[j-9],suits[k])

         # To end up with a one dimensional array of cards
        self.cards = self.cards.flatten()

    def draw_card(self):
        card_index = random.choice(range(self.cards.size))
        card = self.cards[card_index]

        if self.restack == False:
            self.cards = np.delete(self.cards,card_index)

        return card

class Agent:

    def __init__(self, number_of_decks):
        # Maybe we come up with different RL solutions depending on if the agent
        # plays with finite or infinite decks.

        self.difficulty = self.__set_difficulty(number_of_decks)
        self.policy = 'TODO: create policy file'
        self.actions = ['h','s']

    def __set_difficulty(self,number_of_decks):    
        if number_of_decks == 0:
            difficulty = 'easy'
        else:
            difficulty = 'hard'
        
        return difficulty
    
    def select_next_action(self):
        #TODO for now it always hits if the hand sum is less than 19 
        if self.state[0] <= 17:
            return self.actions[0]
        else:
            return self.actions[1]
    
    def update_state(self, hand_sum, value_last_card):
        self.state = [hand_sum, value_last_card]

    def learn_from_action(self, state, action, next_state):
        pass
