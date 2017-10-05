"""
Created 7/7/16

Author:  Sean Benner

Decision rules for using basic strategy in blackjack
"""

import blackjack
import csv

#logic test
def isSplittable(hand):
    if hand[0][0] == hand[1][0] or ((hand[0][0] == 'T' or hand[0][0] == 'J' or hand[0][0] == 'Q' or hand[0][0] == 'K') and (hand[1][0] == 'T' or hand[1][0] == 'J' or hand[1][0] == 'Q' or hand[1][0] =='K')):
        return True
    else:
        return False

#create keys

HardTotalsKey = {}
for x in range(5, 21):
    HardTotalsKey[x] = x-4

SoftTotalsKey = {}
for x in range(13, 22):
    SoftTotalsKey[x] = x-12

SplittableKey = {'A': 10}
SplittableKey['J'] = 9
SplittableKey['Q'] = 9
SplittableKey['K'] = 9
SplittableKey['T'] = 9
for x in range (2, 11):
    SplittableKey[str(x)] = x -1

dealer_key = {}
for x in range(1, 10):
    dealer_key[str(x+1)] = x
for i in 'TJQK':
    dealer_key[i] = 9
dealer_key['A'] = 10



HardTotals = list(csv.reader(open(r'/home/sean/Blackjack/HardTotals.csv')))
SoftTotals = list(csv.reader(open(r'/home/sean/Blackjack/SoftTotals.csv')))
Splittable = list(csv.reader(open(r'/home/sean/Blackjack/Splittable.csv')))

def split(hand, dealer_card):
    choice = Splittable[SplittableKey[hand[0][0]]][dealer_key[dealer_card[0]]]
    if choice == 'X':
        return 'split'
    if choice == 'H':
        return 'hit'
    if choice == 'D':
        return 'double'
    if choice == 'S':
        return 'stand'


def decision(hand, dealer_card, can_double):
    #Decide on hard or soft
    score, soft = blackjack.get_score(hand, True)
    if score == 4:
        return 'hit'
    if score == 21:
        return 'stand'
    if score == 12 and soft:
        return 'hit'
    if soft:
        choice = SoftTotals[SoftTotalsKey[score]][dealer_key[dealer_card[0]]]
        if choice == 'H':
            return 'hit'
        if choice == 'S':
            return 'stand'
        if choice == 'D':
            if can_double:
                return 'double'
            else:
                return 'hit'
        if choice == 'DS':
            if can_double:
                return 'double'
            else:
                return 'stand'
    else:
        choice = HardTotals[HardTotalsKey[score]][dealer_key[dealer_card[0]]]
        if choice == 'H':
            return 'hit'
        if choice == 'S':
            return 'stand'
        if choice == 'D':
            if can_double:
                return 'double'
            else:
                return 'hit'
        if choice == 'DS':
            if can_double:
                return 'double'
            else:
                return 'stand'
