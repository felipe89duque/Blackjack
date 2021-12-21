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
                hand_sum = update_hand_sum(card, hand_history)
                hand_history += [[card, hand_sum]]

                print_hit(card, hand_sum)

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
        raise

def update_hand_sum(card, hand_history):
    new_hand_sum = 0
    num_of_aces = 0
    
    # Add last card to hand_history, just locally for the function
    local_hand_history = hand_history + [[card,new_hand_sum]]

    for i in range(len(local_hand_history)):
        past_card = local_hand_history[i][0]
        if past_card.name == 'A':
            # Count all aces in hand; at the end if possible, add 10 as
            # many times as allowed
            num_of_aces += 1

        new_hand_sum = new_hand_sum + past_card.value
    
    for j in range(num_of_aces):
        if new_hand_sum <= 11:
            new_hand_sum += 10
    
    return new_hand_sum

def print_hit(card, hand_sum):
    if card.name == 'A':
        print("%s\t %s/11\t%s"%(card.name, card.value, hand_sum))
    else:
        print("%s\t %s\t%s"%(card.name, card.value, hand_sum))


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
    print("Card\tValue\tHand sum")
    print("------------------------")


if __name__ == '__main__':
    player = Player()
    decks = Decks(1)
    episode(player,decks)
