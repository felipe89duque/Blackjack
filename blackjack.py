from dependencies import *


def main_menu():
    print('''########################################
Welcome to the simplified Blackjack game!
#########################################''')
    print('''Machine learning in science 1, PHYS4035
Authors: 
- Felipe Duque-Quiceno, Student ID 20377858
- Balázs Nyíro, Student ID (Add)''')
    print('----------------------------------------------')
    print('''
1. To read the rules and learn how to use this program, press '1' followed by 'Enter'.
2. To play yourself, press '2' followed by 'Enter'.
3. To let the trained RL agent play, press '3' followed by 'Enter'.
4. To train the RL agent, press '4' followed by 'Enter'.
NOTE: you can force the program to stop at any point by pressing 'Ctrl'+'C' ''')
    print('----------------------------------------------')
    print('Please enter your choice to proceed')
    action = input()
    if action == '1':
        instructions()
    elif action == '2':
        human_play_episode()
    elif action == '3':
        agent_play_episode()
    elif action == '4':
        agent_train()
    else:
        print('Illegal action! Learn how to follow instructions and try again. >:(')

def instructions():
    print('---------------------------------------------')
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
- For Hit, enter the character 'h' followed by 'Enter'.
- For Stick, enter the character 's' followed bu 'Enter'.

The program can be forced to stop at any point by pressing Ctrl+C.
''')
    print("Press 'Enter' to go back to the main menu")
    _ = input()
    main_menu()

def human_play_episode():
    print('---------------------------------------------')
    print("Welcome fellow human")
    while True:
        print("Let's start by choosing the number of decks you want to play with. 0 is equivalent to infinitely many decks (easy version).")
        num_of_decks = input("# of decks: ")
        try:
            num_of_decks = int(num_of_decks)
            break
        except:
            print("Either you didn't understand me, or didn't understand you, let's try this again...")
    play_episode(num_of_decks,'human')

def agent_play_episode():
    print('---------------------------------------------')
    print("Watch and learn, my baby agent is a pro at this game")
    while True:
        print("Let's start by choosing the number of decks you want the agent to play with. 0 is equivalent to infinitely many decks (easy version).")
        num_of_decks = input("# of decks: ")
        try:
            num_of_decks = int(num_of_decks)
            break
        except:
            print("Either you didn't understand me, or didn't understand you, let's try this again...")
    play_episode(num_of_decks,'agent')

def agent_train():
    print('TODO')

def play_episode(difficulty,who_is_playing):
    global decks
    global hands_played
    global episode_sum
    global hand_sum
    global stop_hand
    global stop_episode

    episode_sum = 0
    hand_sum = 0
    stop_hand = False
    stop_episode = False

    decks = Decks(difficulty)
    hands_played = 0 # Number of hands played
    
    while stop_episode == False:
        hands_played += 1
        play_hand(who_is_playing)

    print("You are out of cards! Your final score is %s\nThank you for playing. :D"%(episode_sum))

def play_hand(who_is_playing):
    global episode_sum
    global hands_played

    print("#######################")
    print("Hand # %s"%(hands_played))
    print("Card | Value | Hand sum")
    print("-----------------------")
    
    hit() # First card
    try:
        while True:
            if stop_hand:
                hand_score = get_hand_score()
                episode_sum += hand_score
                break
            else:
                action = select_next_action(who_is_playing)
                do_action(action)
    except NameError:
        print("Something went wrong:")
        raise

    print("-----------------------")
    print("Hand score:", hand_score,"\nEpisode score: ",episode_sum,"\n\n")
    reset_hand()

def select_next_action(who_is_playing):
    if who_is_playing == 'human':
        action = input('(h/s):\t')
    elif who_is_playing == 'agent':
        raise NameError("TODO: This code does not exist yet.")
    else:
        raise NameError("You should not be here!!! There is a bug somewhere!")
    return action

def do_action(action):
    if action =='h':
        hit()
    elif action == 's':
        stick()

def hit():
    global hand_sum
    
    check_if_gameover()
    card = decks.draw_card()
   
    # Check if A's and give respective value
    if (card.name == 'A'):
        if (hand_sum + 11 > 21):
            card.value = 1
        else:
            card.value = 11

    hand_sum += card.value
    check_if_gameover()

    print( card.name,'\t', card.value,'\t', hand_sum)

def stick():
    global stop_hand
    stop_hand = True

def check_if_gameover():
    global stop_hand
    global stop_episode

    # Check if the sum is equal or over 21
    if (hand_sum >= 21):
        stop_hand = True
    else:
        stop_hand = False

    # Check if the decks are empty
    if decks.cards.size == 0:
        stop_hand = True
        stop_episode = True

def get_hand_score():
    if (hand_sum <= 21):
        hand_score = hand_sum**2
    else:
        hand_score = 0
    return hand_score

def reset_hand():
    global hand_sum
    global stop_hand

    hand_sum = 0
    stop_hand = False


if __name__ == '__main__':
    main_menu()
