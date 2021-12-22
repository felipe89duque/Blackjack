from blackjack import *


def main_menu():
    print('''
#################################################################################

Welcome to the simplified Blackjack game!

#################################################################################''')
    print('''Machine learning in science 1, PHYS4035
Authors: 
- Felipe Duque-Quiceno, Student ID 20377858
- Balázs Nyíro, Student ID (Add)''')
    print('---------------------------------------------------------------------')
    print('''
1. To read the rules and learn how to use this program, press '1' followed by ENTER.
2. To play yourself, press '2' followed by ENTER.
3. To let the trained RL agent play, press '3' followed by ENTER.
4. To train the RL agent, press '4' followed by ENTER.
NOTE: you can force the program to stop at any point by pressing Ctrl+C ''')
    print('---------------------------------------------------------------------')
    print('Please enter your choice to proceed')
    action = input()
    if action == '1':
        instructions()
    elif action == '2':
        human_play_episode()
    elif action == '3':
        agent_play_episode()
    elif action == '4':
        verify_access()
    else:
        print('Illegal action! Learn how to follow instructions and try again. >:(')
        go_back_to_menu()

def instructions():
    print('---------------------------------------------------------------------')
    print("Rules:")
    print('''
- There is only one player (either you OR a trained agent).
- The game is played with D decks of Poker (52 cards per deck: 2-10 plus
  J/Q/K/A per suit).
- You choose the number of decks D (infinite decks is a possibility). 
- The value of each card is its number. J, Q and K have all a value of 10.
- Aces have a value of 11 unless the hand sum goes over 21, then its
  value is of 1.
- The game lasts until all cards are used.
- The aim of the game is to maximize the accumulated score. This is the addition
  of the score of all hands played.
- The score of a hand is: the square of the hand sum, if this is lower or equal
  to 21; 0 if the hand sum goes over 21... In other words, try to get as close
  to 21 as possible without passing it.
- Whenever a new card is dealt, its value is added to the hand sum.
- When a card is dealt, there are two possible actions to choose from: Hit (h)
  or Stick (s). Hit means that a new card will be dealt, Stick means that the
  hand will end at the current hand sum.\n\n''')

    print("How to use the program:")
    print('''
At the main menu, choose whether you want to play blackjack, or see how a
reinforcement learning (RL) trained agent plays by itself. In any case, you then
must choose the number of decks of cards to play with. To play with infinitely
many cards, choose '0' as the number of decks (You may want to play in this
setting as the 'easy' version, as the likelyhood of any card being dealt does
not change over time). 

At this point, an episode of blackjack will start. If you chose to see the
agent play, enjoy. If you chose to play yourself, bare in mind that after each
card deal you must select the next action (hit or stick). 
- For Hit, enter the character 'h' followed by ENTER.
- For Stick, enter the character 's' followed bu ENTER.

The program can be forced to stop at any point by pressing Ctrl+C.
''')
    go_back_to_menu()

def human_play_episode():
    print('---------------------------------------------------------------------')
    print("Welcome fellow human")
    
    num_of_decks = set_difficulty()
    player, decks = create_player_and_decks('human', num_of_decks)  
    episode(player, decks)

def agent_play_episode():
    print('---------------------------------------------------------------------')
    print("Watch and learn, my baby agent is a pro at this game")

    num_of_decks = set_difficulty('the agent')
    player, decks = create_player_and_decks('agent', num_of_decks)
    episode(player, decks)

def agent_train():
    num_of_decks = int(input("# of decks: ")) 
    player, decks = create_player_and_decks('agent', num_of_decks, agent_sleep = False)
    # TODO while True?
    trajectory = episode(player, decks, training = True)
    player.learn(trajectory)
    print(trajectory)
        

def create_player_and_decks(agent_or_human, number_of_decks, agent_sleep = True):
    if agent_or_human == 'human':
        player = Player()
    elif agent_or_human == 'agent':
        player = Agent(number_of_decks, sleep = agent_sleep)

    decks = Decks(number_of_decks)

    return (player, decks)

def set_difficulty(player = '\b'):                                                 
    while True:                                                                  
        print("\nInsert the number of decks you want %s to play with. 0 is equivalent to infinitely many decks (easy version)."%(player)) 
        num_of_decks = input("# of decks: ")                                     
        try:                                                                     
            num_of_decks = int(num_of_decks)                                     
            break                                                                
        except:                                                                  
            print("Either you didn't understand me, or didn't understand you, let's try this again...    ")  
    return num_of_decks 

def verify_access():
    easy_password = "MLIS2021_Balazs_Felipe"
    print("Training an agent overrides important data! Insert password to continue ")
    password= input("Password: ")
    if password == easy_password:
        print("Welcome back Sensei, let's train!")
        agent_train()
    else:
        print("Sorry! You don't have access to these functionalities.")
        go_back_to_menu()
        

def go_back_to_menu():
    print("Press ENTER to go back to the main menu.")
    _ = input()
    main_menu()


if __name__ == '__main__':
    main_menu()
