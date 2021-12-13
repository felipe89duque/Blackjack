from dependencies import *

card_names = np.array(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])
suits = np.array(["Spades","Hearts","Clubs","Diamonds"])
card_values = np.array([2,3,4,5,6,7,8,9,10,10,10,10,11,1]) # A's can have a value of 1 (first index), or 11 (last index), depending on sum

decks = Decks() 

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

def do_action(action):
    if action =='h':
        hit()
    elif action == 's':
        stick()

def play_hand():
    global episode_sum
    global cont

    print("#######################")
    print("Hand # %s"%(cont))
#    print("-----------------------")
    print("Card | Value | Hand sum")
    print("-----------------------")
    
    hit() # First card
    
    while True:
        if stop_hand:
            hand_score = get_hand_score()
            episode_sum += hand_score
            break
        else:
            action = input("(h/s):\t")
            do_action(action)

    print("-----------------------")
    print("Hand score:", hand_score,"\nEpisode score: ",episode_sum,"\n\n")
    reset_hand()

cont = 0 # Number of hands played
while True:
    cont += 1
    play_hand()
