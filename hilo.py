
def true_count(r_count, shoe):
    return float(r_count)/(len(shoe)/52.0)

def running_count(hands, current_count):
    count = current_count
    for hand in hands:
        for card in hand:
            if card[0] == '2' or card[0] == '3' or card[0] == '4' or card[0] == '5' or card[0] == '6':
                count += 1
            if card[0] == 'T' or card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' or card[0] == 'A':
                count -= 1
    return count

def bet_amount(count, shoe, unit_bet):
    TC = true_count(count, shoe)
    if TC < -2:
        return 0
    elif -2 <= TC <= 0:
        return unit_bet/2.0
    elif 0 < TC:
        return (TC - 1) * unit_bet
