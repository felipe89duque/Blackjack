import time
import numpy as np
import random
import pandas as pd

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
                value = 1
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

class Player:
    def __init__(self):
        self.actions = ['s','h']
    
    def select_next_action(self):
        action = input('(h/s):\t')
        return action

    def update_state(self, new_state):
        self.state = new_state

class Agent(Player):
    def __init__(self, number_of_decks, sleep = True, epsilon = 0):
        super().__init__()
        self.difficulty = self.__set_difficulty(number_of_decks)
        
        # Determine if the agents sleeps before it chooses an action, when
        # training, it is set False by the constructor
        self.sleep = sleep       
        self.epsilon = epsilon
        self.Q = self.__get_state_action_values()

    def __set_difficulty(self,number_of_decks):    
        if number_of_decks == 0:
            difficulty = 'easy'
        else:
            difficulty = 'hard'
        
        return difficulty

    def __get_state_action_values(self):
        try:
            if self.difficulty == 'easy':
                Q = pd.read_csv("tabular_Q_As.csv",index_col=0)
            else:
                raise NotImplementedError

            return Q
        except NotImplementedError:
            print("The agent hasn't been programmed to know how to play with finite decks yet!")
    
    def select_next_action(self):
        if self.sleep:
            time.sleep(1)

        # Tabular method:
        if self.difficulty == 'easy':

            # epsilon-greedy
            action_index, _ = self.__get_max_value_action(self.state)

            # epsilon likelihood of exploring
            if random.random() <= self.epsilon:
                action_index = 1-action_index

            return self.actions[action_index]
        else:
            print("The agent hasn't been programmed to know how to play with finite decks yet!")

    def learn(self, trajectory):
        # get number of training sessions and add 1
        with open("tabular_As_episodes_trained.txt","r") as training_index_file:
            last_training_index = int(training_index_file.read()) + 1


        # find last exploratory action
        index_last_exploration = 0
        for i in range(len(trajectory)-1):
            state = trajectory[i][0]

            action = trajectory[i][2]
            numeric_action = self.actions.index(action)
            _, max_value = self.__get_max_value_action(state)

            if max_value != self.__get_state_action_value(state,numeric_action):
                # Action was chosen non-greedily (exploration)
                index_last_exploration = i

        # Evaluate trajectory from the end towards the last exploration
        total_reward = 0
        for i in range(len(trajectory)-2,index_last_exploration-1,-1):
            state = trajectory[i][0]
            action = trajectory[i][2]
            numeric_action = self.actions.index(action)
            self.__increment_times_visited(state, numeric_action)
            
            reward = trajectory[i+1][1]
            total_reward += reward
            
            current_value = self.__get_state_action_value(state, numeric_action)
            n = self.__get_times_visited(state, numeric_action)
            new_value = current_value + (1/n)*(total_reward - current_value)

            self.__set_new_state_action_value(state, numeric_action, new_value)



        # add new Q to history file
        Q_last_session = self.Q.copy()
        Q_last_session.loc[:,"training index"] = last_training_index
        
        with open("tabular_Q_As.csv","w") as Q_file:
            Q_file.write(self.Q.to_csv())
        with open("tabular_Q_As_history.csv","a") as Q_history_file:
            Q_history_file.write(Q_last_session.to_csv(header=False))
        with open("tabular_As_episodes_trained.txt","w") as training_index_file:
            training_index_file.write(str(last_training_index))

    def __get_max_value_action(self,state):
        hand_sum = state[0]
        usable_A = state[1]

        action_values = self.Q[["action","value"]].loc[(self.Q["usable A"] == usable_A) &\
                                                       (self.Q["hand sum"] == hand_sum)]
        
        max_value = action_values["value"].max()
        # if both actions have same value, choose randomly
        action_indices = action_values["action"].loc[action_values["value"]==max_value].values
        action_index = np.random.choice(action_indices)

        return action_index, max_value

    def __get_state_action_value(self,state,action):
        hand_sum = state[0]
        usable_A = state[1]

        value = self.Q.loc[(self.Q["usable A"] == usable_A) &\
                           (self.Q["hand sum"] == hand_sum) &\
                           (self.Q["action"] == action),\
                           "value"].values[0]
        
        return value

    def __get_times_visited(self,state,action):
        hand_sum = state[0]
        usable_A = state[1]

        times_visited = self.Q.loc[(self.Q["usable A"] == usable_A) &\
                                   (self.Q["hand sum"] == hand_sum) &\
                                   (self.Q["action"] == action),\
                                    "times visited"].values[0]

        return times_visited

    def __increment_times_visited(self, state, action):
        hand_sum = state[0]
        usable_A = state[1]

        self.Q.loc[(self.Q["usable A"] == usable_A) &\
                   (self.Q["hand sum"] == hand_sum) &\
                   (self.Q["action"] == action),\
                    "times visited"] += 1
    
    def __set_new_state_action_value(self, state, action, new_value):
        hand_sum = state[0]
        usable_A = state[1]

        self.Q.loc[(self.Q["usable A"] == usable_A) &\
                   (self.Q["hand sum"] == hand_sum) &\
                   (self.Q["action"] == action),\
                    "value"] = new_value
