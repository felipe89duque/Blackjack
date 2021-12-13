import numpy as np
import random

card_names = np.array(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])
suits = np.array(["Spades","Hearts","Clubs","Diamonds"])
card_values = np.array([2,3,4,5,6,7,8,9,10,10,10,10,11,1]) # A's can have a value of 1 (first index), or 11 (last index), depending on sum

episode_sum = 0
hand_sum = 0
stop_hand = False

def check_if_gameover():
    global stop_hand
    if (hand_sum >= 21):
        stop_hand = True
    else:
        stop_hand = False

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

def hit():
    global hand_sum

    card = random.choice(card_names)
    card_index = np.where(card_names == card)[0][0]
    value = card_values[card_index]
    provitional_sum = hand_sum + value

    # Check if As:
    if (card == 'A'):
        if (provitional_sum > 21):
            value = 1
        
    hand_sum += value
    
    check_if_gameover()

    print( card,'\t', value,'\t', hand_sum)

def stick():
    global stop_hand
    stop_hand = True

def do_action(action):
    if action =='h':
        hit()
    elif action == 's':
        stick()

def play_hand():
    global episode_sum

    print("Card | Value | Hand sum \n ----------------------")
    
    hit() # First card
    
    while True:
        if stop_hand:
            hand_score = get_hand_score()
            episode_sum += hand_score
            break
        else:
            action = input("h/s:\t")
            do_action(action)


    print("Hand score:", hand_score,"\nEpisode score: ",episode_sum,"\n\n")
    reset_hand()

while True:
    play_hand()
