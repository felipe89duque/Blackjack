from dependencies import *

def episode(player, decks, training = False):
    try:
        hand_sum = 0
        episode_score = 0
        action = 'h'
        num_of_hands = 0
        
        hand_history = []

        print_next_hand(num_of_hands)

        while True:
            if len(hand_history) == 0:
                action = 'h'
            else:
                action = player.select_next_action()
            
            if action == 'h':
                card = decks.draw_card()
                card.assign_value_if_A(hand_sum) #TODO: As value changes through hand
                hand_sum += card.value

                hand_history += [[action, card, hand_sum]]
                print("%s \t %s \t %s"%(card.name, card.value, hand_sum))
                if hand_sum >=21:
                    end_hand = True
                else:
                    end_hand = False
            elif action == 's':
                end_hand = True

            # The player updates its state according to the last step
            player.update_state(hand_history[-1])

            if end_hand:
                hand_score = get_hand_score(hand_sum)
                episode_score += hand_score
                print_end_of_hand(hand_score,episode_score)
                hand_history = []
                end_hand = False

                if training:
                    player.learn(hand_history)

                num_of_hands += 1
                hand_sum = 0
                print_next_hand(num_of_hands)
    except:
        print("Final score: %s"%(episode_score))
        #raise

def get_hand_score(hand_sum):
    if (hand_sum <= 21):
        hand_score = hand_sum**2
    else:
        hand_score = 0
    return hand_score

def print_end_of_hand(hand_score,episode_score):
    print("Hand score: %s | Episode score: %s"%(hand_score,episode_score))

def print_next_hand(num_of_hands):
    print("\n\n")
    print("________________________")
    print("Hand # %s:"%(num_of_hands))
    print("Card  | Value  | Hand sum")


if __name__ == '__main__':
    player = Player()
    decks = Decks(1)
    episode(player,decks)
